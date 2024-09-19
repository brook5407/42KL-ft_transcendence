import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Player, TournamentRoom, Match, TournamentPlayer, TournamentMatch, UserActiveTournament
from asgiref.sync import async_to_sync
from django.utils import timezone


gameHeight = 500
gameWidth = 800

class MatchManager:
    def __init__(self):
        '''
            players: {
                channel_name: player_id,
            }
        '''
        self.players = {}  # maximum 2 players

        self.paddle1 = Paddle(20, 200, 10, 100)
        self.paddle2 = Paddle(gameWidth - 30, 200, 10, 100)
        self.ball = Ball(400, 250, 8, 5)
        self.score1 = 0
        self.score2 = 0

    def add_player(self, channel_name, player_id):
        if len(self.players) >= 2:
            return
        self.players[channel_name] = player_id

    def remove_player(self, channel_name):
        self.players.pop(channel_name, None)
            
    def get_player_id_from_channel_name(self, channel_name):
        player_id = self.players.get(channel_name, None)
        return player_id
            
    def get_players_channels(self):
        return self.players.keys()


class RoomManager:
    rooms = {}  # A dictionary to map room ids to their respective managers

    @classmethod
    def get_match_manager(cls, room_id) -> MatchManager:
        if room_id not in cls.rooms:
            cls.rooms[room_id] = MatchManager()
        return cls.rooms[room_id]

    @classmethod
    def remove_room(cls, room_id):
        if room_id in cls.rooms:
            del cls.rooms[room_id]


class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.game_mode = self.scope['url_route']['kwargs']['game_mode']
        self.room_id = self.scope['url_route']['kwargs']['room_id'] # room_id is the match_id
        self.room_group_name = f'pong_{self.room_id}'
        self.paddle = None
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        self.manager = RoomManager.get_match_manager(self.room_id)
        self.player = await self.get_player(self.user)
        self.manager.add_player(self.channel_name, self.player.id)

        if (self.game_mode == "pvp"):
            await self.wait_for_opponent()
        elif (self.game_mode == "pve"):
            await self.pve_mode()
            
    @database_sync_to_async
    def get_player(self, user):
        return Player.objects.get(user=user)
            
    async def wait_for_opponent(self):
        while len(self.manager.players) < 2:
            return
        await self.pvp_mode()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        movement = data.get('movement')
        if not movement:
            return
        
        velocity = 0
        if movement == 'up':
            velocity = -10
        elif movement == 'down':
            velocity = 10
        elif movement == 'stop':
            velocity = 0

        # Update the paddle's velocity
        if self.paddle == 'paddle1':
            self.manager.paddle1.velocity = velocity
        elif self.paddle == 'paddle2':
            self.manager.paddle2.velocity = velocity

    async def pvp_mode(self):
        self.player1, self.player2 = self.manager.get_players_channels()

        await self.channel_layer.send(self.player1, {
            'type': 'paddle_assignment',
            'message': 'You are Paddle 1!',
            'paddle': 'paddle1',
        })
        await self.channel_layer.send(self.player2, {
            'type': 'paddle_assignment',
            'message': 'You are Paddle 2!',
            'paddle': 'paddle2',
        })

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'start_game',
                'message': 'Game had started!',
            })
        asyncio.create_task(self.game_loop())

    async def pve_mode(self):
        self.player1 = self.channel_name
        self.player2 = "computer"
        await self.channel_layer.send(self.player1, {
            'type': 'paddle_assignment',
            'message': 'You are Paddle 1!',
            'paddle': 'paddle1',
        })
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'start_game',
            'message': 'channel_layer.group_send: start_game',
        })
        asyncio.create_task(self.game_loop())

    async def paddle_assignment(self, event):
        self.paddle = event['paddle']
        await self.send(text_data=json.dumps({
            'type': 'paddle_assignment',
            'message': event['message'],
            'paddle': event['paddle'],
        }))

    async def start_game(self, event):
        print("start_game")
        await self.send(text_data=json.dumps({
            'type': 'start_game',
            'message': event['message'],
            'gameHeight': gameHeight,
            'gameWidth': gameWidth,
            'paddle1': self.manager.paddle1.serialize(),
            'paddle2': self.manager.paddle2.serialize(),
            'ball': self.manager.ball.serialize(),
        }))
        for i in range(3, 0, -1):
            await self.send(text_data=json.dumps({
                'type': 'countdown_game',
                'message': i,
            }))
            await asyncio.sleep(1)

    async def game_loop(self):
        winner_channel = None
        winner_score = 0
        loser_score = 0
        await asyncio.sleep(4)
        while True:
            # Update game state
            self.manager.ball.move()
            self.manager.paddle1.move()
            self.manager.paddle2.move()

            # AI Paddle follows the ball
            if (self.game_mode == "pve"):
                self.manager.paddle2.follow_ball(self.manager.ball)

            # Check for scoring
            if self.manager.ball.x <= 0:
                self.manager.score2 += 1
                self.reset_ball()
            elif self.manager.ball.x >= gameWidth:
                self.manager.score1 += 1
                self.reset_ball()

            # Collision for paddle and top and bottom of game canvas
            self.manager.ball.check_collision(self.manager.paddle1, self.manager.paddle2)

            # Broadcast game state to clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_game_state',
                    'paddle1': self.manager.paddle1.serialize(),
                    'paddle2': self.manager.paddle2.serialize(),
                    'ball': self.manager.ball.serialize(),
                    'score1': self.manager.score1,
                    'score2': self.manager.score2,
                }
            )

            winningScore = 3

            # End the game if a player reaches a score of winningScore
            if self.manager.score1 >= winningScore or self.manager.score2 >= winningScore:
                winner = 'Player 1' if self.manager.score1 >= winningScore else 'Player 2'
                loser = self.player2 if self.manager.score1 >= winningScore else self.player1
                winner_channel = self.player1 if self.manager.score1 >= winningScore else self.player2
                winner_score = self.manager.score1 if self.manager.score1 >= winningScore else self.manager.score2
                loser_score = self.manager.score2 if self.manager.score1 >= winningScore else self.manager.score1
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'end_game',
                        'message': f'{winner} wins!',
                        'loser': loser,
                    }
                )
                break  # Exit the game loop

            await asyncio.sleep(1/60)  # Run at ~60 FPS
        winner_player_id = self.manager.get_player_id_from_channel_name(winner_channel)
        await self.set_match_end(winner_player_id, winner_score, loser_score)
    
    @database_sync_to_async
    def set_match_end(self, winner_player_id, winner_score, loser_score):
        match = Match.objects.get(id=self.room_id)
        placeholder_winner = match.winner
        placeholder_loser = match.loser
        if winner_player_id != placeholder_winner.id:
            match.winner = placeholder_loser
            match.loser = placeholder_winner
        match.winner.add_win()
        match.loser.add_loss()
        match.winner_score = winner_score
        match.loser_score = loser_score
        match.ended_at = timezone.now()
        match.save()

    async def update_game_state(self, event):
        # Send updated game state to WebSocket
        await self.send(text_data=json.dumps({
            'type' : 'update_game_state',
            'paddle1': event['paddle1'],
            'paddle2': event['paddle2'],
            'ball': event['ball'],
            'score1': event['score1'],
            'score2': event['score2'],
        }))

    async def end_game(self, event):
        self.manager.remove_player(event['loser'])
        await self.send(text_data=json.dumps({
            'type': 'end_game',
            'message': event['message'],
        }))
            

    def reset_ball(self):
        self.manager.ball = Ball(400, 250, 8, 5)

    def reset_paddles(self):
        self.manager.paddle1 = Paddle(20, 200, 10, 100)
        self.manager.paddle2 = Paddle(gameWidth - 30, 200, 10, 100)

    def reset_score(self):
        self.manager.score1 = 0
        self.manager.score2 = 0

    def reset_game(self):
        self.reset_ball()
        self.reset_paddles()
        self.reset_score()


class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0
        self.speed = 10
        self.mid_x = self.x + (self.width / 2)
        self.mid_y = self.y + (self.height / 2)

    def move(self):
        self.y += self.velocity
        # Keep paddle within bounds
        if self.y < 0:
            self.y = 0
        if self.y > gameHeight - self.height:
            self.y = gameHeight - self.height

    def follow_ball(self, ball):
        # If ball is below paddle, move down
        if ball.y > self.y + self.height:
            self.velocity = self.speed
        # If ball is above paddle, move up
        elif ball.y < self.y:
            self.velocity = -self.speed

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
        }

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.oriSpeed = speed
        self.x_direction = random.choice([-1, 1])
        self.y_direction = random.choice([-1, 1])

    def move(self):
        self.x += self.speed * self.x_direction
        self.y += self.speed * self.y_direction

    def check_collision(self, paddle1, paddle2):
        # Y-axis collision with the top and bottom of the game area
        if (self.y <= 0 and self.y_direction < 0) or (self.y >= gameHeight and self.y_direction > 0):
            self.y_direction *= -1

        # Paddle 1 collision (left paddle)
        if (self.x <= paddle1.x + paddle1.width + self.radius and 
            paddle1.y <= self.y <= paddle1.y + paddle1.height):
            
            self.x_direction = 1  # Ball goes to the right

            # Calculate the impact point on the paddle relative to its center
            hit_pos = (self.y - (paddle1.y + paddle1.height / 2)) / (paddle1.height / 2)

            # Adjust y-direction based on where the ball hits the paddle
            if hit_pos > 0.5:  # Bottom quarter
                self.y_direction = 1  # Steeper downward angle
            elif hit_pos > 0:  # Bottom center
                self.y_direction = 0.5  # Shallow downward angle
            elif hit_pos > -0.5:  # Top center
                self.y_direction = -0.5  # Shallow upward angle
            else:  # Top quarter
                self.y_direction = -1  # Steeper upward angle
            self.speed = min(self.speed + 1, 15)

        # Paddle 2 collision (right paddle)
        if (self.x >= paddle2.x - self.radius and 
            paddle2.y <= self.y <= paddle2.y + paddle2.height):
            
            self.x_direction = -1  # Ball goes to the left

            # Calculate the impact point on the paddle relative to its center
            hit_pos = (self.y - (paddle2.y + paddle2.height / 2)) / (paddle2.height / 2)

            # Adjust y-direction based on where the ball hits the paddle
            if hit_pos > 0.5:  # Bottom quarter
                self.y_direction = 1  # Steeper downward angle
            elif hit_pos > 0:  # Bottom center
                self.y_direction = 0.5  # Shallow downward angle
            elif hit_pos > -0.5:  # Top center
                self.y_direction = -0.5  # Shallow upward angle
            else:  # Top quarter
                self.y_direction = -1  # Steeper upward angle
            self.speed = min(self.speed + 1, 15)


    def serialize(self):
        return {
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
        }

class MatchMakingConsumer(AsyncWebsocketConsumer):
    """
        ELO Rating System:

        Ea = 1 / (1 + 10^((Rb - Ra) / 400))
        Eb = 1 / (1 + 10^((Ra - Rb) / 400))
        Ra' = Ra + K * (Sa - Ea)
        Rb' = Rb + K * (Sb - Eb)
        where:
            - Ra and Rb are the ratings of players A and B, respectively.
            - Ea and Eb are the expected scores of players A and B, respectively.
            - Sa and Sb are the actual scores of players A and B, respectively. (1 for win, 0 for loss)
            - K is the weight constant (e.g., 32 for chess).
        In tournament play, just add/sub a fixed value (e.g. 32) to the winner/loser.

        Range for Matching:
        Match players with others within ±100 Elo points.
        As the waiting time increases, can expand the range, but not more than ±200 Elo points.
    """
    
    '''
        connected_players: {
            player_id: {
                channel_name: channel_name,
                elo: elo,
            }
        }
    '''
    connected_players = {}
    
    async def connect(self):
        self.user = self.scope['user']
        player = await self.get_player(self.user)
        if player:
            self.player_id = await self.get_player_id(player)
            if self.player_id in self.connected_players:
                await self.close()
                return
            await self.channel_layer.group_add('matchmaking', self.channel_name)
            await self.accept()
            self.connected_players[self.player_id] = {
                'channel_name': self.channel_name,
                'elo': await self.get_player_elo(player)
            }
            print(self.connected_players)
            await self.match_player(player)
        else:
            await self.close()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('matchmaking', self.channel_name)
        self.connected_players.pop(self.player_id, None)
    
    async def receive(self, text_data):
        data = json.loads(text_data)

    @database_sync_to_async
    def get_player_id(self, player):
        return player.id

    @database_sync_to_async
    def get_player(self, user):
        return Player.objects.get(user=user)
    
    @database_sync_to_async
    def get_player_elo(self, player):
        return player.elo
    
    @database_sync_to_async
    def create_match(self, player, opponent_player_id):
        match = Match.objects.create(
            winner=player,
            loser_id=opponent_player_id,
            type=Match.MatchType.PVP
        )
        return match

    async def match_player(self, player):
        elo_range = 100

        player_elo = await self.get_player_elo(player)
        min_elo = player_elo - elo_range
        max_elo = player_elo + elo_range

        potential_opponents = [
            (player_id, player_info['channel_name']) for player_id, player_info in self.connected_players.items()
            if min_elo <= player_info['elo'] <= max_elo and player_info['channel_name'] != self.channel_name
        ]

        if potential_opponents:
            opponent_channel_name = potential_opponents[0][1]
            match = await self.create_match(player, potential_opponents[0][0])
            
            # Inform the opponent
            await self.channel_layer.send(
                opponent_channel_name,
                {
                    'type': 'start_match',
                    'match_id': match.id,
                }
            )
            
            await self.channel_layer.send(
                self.channel_name,
                {
                    'type': 'start_match',
                    'match_id': match.id,
                }
            )
            
    async def start_match(self, event):
        match_id = event['match_id']
        await self.send(text_data=json.dumps({
            'type': 'start_match',
            'match_id': match_id,
        }))
            

    def calculate_elo(self, Ra, Rb, Sa, Sb, K=32):
        Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
        Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
        Ra_new = Ra + K * (Sa - Ea)
        Rb_new = Rb + K * (Sb - Eb)
        return Ra_new, Rb_new
    

class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.tournament_id = None
        self.tournament_group_name = None
        self.tournament : TournamentRoom|None = None
        
        await self.set_user_active_tournament()
        await self.accept()

    async def disconnect(self, close_code):
        if self.is_in_tournament():
            await self.channel_layer.group_discard(self.tournament_group_name, self.channel_name)
            self.clear_tournament()

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get('type')
        if type == 'create_tournament':
            await self.create_tournament(data)
        elif type == 'join_tournament':
            await self.join_tournament(data)
        elif type == 'leave_tournament':
            await self.leave_tournament(data)
        elif type == 'start_tournament':
            await self.start_tournament(data)
        elif type == 'rejoin_tournament':
            await self.rejoin_tournament(data)
    
    def is_in_tournament(self):
        return self.tournament_group_name is not None
    
    @database_sync_to_async
    def set_user_active_tournament(self):
        active_tournament = UserActiveTournament.objects.get(user=self.user)
        if active_tournament.tournament is not None:
            self.tournament_id = active_tournament.tournament.id
            self.tournament_group_name = f'tournament_{self.tournament_id}'
            self.tournament = active_tournament.tournament
            async_to_sync(self.channel_layer.group_add)(self.tournament_group_name, self.channel_name)
            async_to_sync(self.channel_layer.group_send)(
                self.tournament_group_name,
                {
                    'type': 'player_rejoined',
                    'user_id': self.user.id,
                    'message': f'User {self.user.username} re-joined the room.',
                    'tournament_id': self.tournament_id,
                }
            )
    
    async def create_tournament(self, event):
        if self.is_in_tournament():
            return
        tournament_id = event['tournament_id']
        self.tournament_id = tournament_id
        self.tournament_group_name = f'tournament_{self.tournament_id}'
        self.tournament = await database_sync_to_async(TournamentRoom.objects.get)(id=tournament_id)
        await self.channel_layer.group_add(self.tournament_group_name, self.channel_name)
    
    async def join_tournament(self, event):
        if self.is_in_tournament():
            return
        tournament_id = event['tournament_id']
        self.tournament_id = tournament_id
        self.tournament_group_name = f'tournament_{self.tournament_id}'
        self.tournament = await database_sync_to_async(TournamentRoom.objects.get)(id=tournament_id)
        await self.channel_layer.group_add(self.tournament_group_name, self.channel_name)

        await self.channel_layer.group_send(
            self.tournament_group_name,
            {
                'type': 'player_joined',
                'user_id': self.user.id,
                'message': f'User {self.user.username} joined the tournament.',
                'tournament_id': self.tournament_id,
            }
        )
    
    async def leave_tournament(self, event):
        if not self.is_in_tournament():
            return
        # if user is the owner, delete the tournament
        if await self.is_owner():
            # await database_sync_to_async(self.tournament.delete)()
            await self.channel_layer.group_send(
                self.tournament_group_name,
                {
                    'type': 'owner_left',
                    'message': 'The owner has left the tournament room. The tournament has been canceled.',
                    'tournament_id': self.tournament_id,
                }
            )
            await self.channel_layer.group_discard(self.tournament_group_name, self.channel_name)
            self.clear_tournament()
            return

        # await database_sync_to_async(self.tournament.remove_player)(self.user)
        await self.channel_layer.group_send(
            self.tournament_group_name,
            {
                'type': 'player_left',
                'user_id': self.user.id,
                'message': f'User {self.user.username} left the tournament room.',
                'tournament_id': self.tournament_id,
            }
        )
        await self.channel_layer.group_discard(self.tournament_group_name, self.channel_name)
        self.clear_tournament()
        
    async def start_tournament(self, event):
        if not self.is_in_tournament():
            return
        if not await self.is_owner():
            return
        try:
            await database_sync_to_async(self.tournament.start)()
        except ValueError as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e),
            }))
            return
        await self.channel_layer.group_send(
            self.tournament_group_name,
            {
                'type': 'tournament_started',
                'message': 'Tournament has started.',
                'tournament_id': self.tournament_id,
            }
        )
        
    async def rejoin_tournament(self, event):
        if self.is_in_tournament():
            return
        tournament_id = event['tournament_id']
        self.tournament_id = tournament_id
        self.tournament_group_name = f'tournament_{self.tournament_id}'
        self.tournament = await database_sync_to_async(TournamentRoom.objects.get)(id=tournament_id)
        await self.channel_layer.group_add(self.tournament_group_name, self.channel_name)
        await self.channel_layer.group_send(
            self.tournament_group_name,
            {
                'type': 'player_rejoined',
                'user_id': self.user.id,
                'message': f'User {self.user.username} re-joined the room.',
                'tournament_id': self.tournament_id,
            }
        )
        
    def clear_tournament(self):
        self.tournament_id = None
        self.tournament_group_name = None
        self.tournament = None
    
    @database_sync_to_async
    def is_owner(self):
        return self.user == self.tournament.owner
        
    async def player_joined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_joined',
            'user_id': event['user_id'],
            'message': event['message'],
            'tournament_id': event['tournament_id'],
        }))
        
    async def player_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_left',
            'user_id': event['user_id'],
            'message': event['message'],
            'tournament_id': event['tournament_id'],
        }))
        
    async def owner_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'owner_left',
            'message': event['message'],
            'tournament_id': event['tournament_id'],
        }))
        
    async def player_rejoined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_rejoined',
            'user_id': event['user_id'],
            'message': event['message'],
            'tournament_id': event['tournament_id'],
        }))
        
    async def tournament_started(self, event):
        await self.send(text_data=json.dumps({
            'type': 'tournament_started',
            'message': event['message'],
            'tournament_id': event['tournament_id'],
        }))
