import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Player, TournamentRoom, Match, TournamentPlayer, TournamentMatch, UserActiveTournament
from asgiref.sync import async_to_sync


gameHeight = 500
gameWidth = 800

class MatchManager:
    matches = {}
    player_counter = 0

    @classmethod
    def assign_player_id(cls):
        cls.player_counter += 1
        return cls.player_counter

    @classmethod
    def create_match(cls, room_name):
        if room_name not in cls.matches:
            cls.matches[room_name] = {
                'player1': None,
                'player2': None,
                'paddle1': Paddle(20, 200, 10, 100),
                'paddle2': Paddle(gameWidth - 30, 200, 10, 100),
                'ball': Ball(400, 250, 8, 5),
                'score1': 0,
                'score2': 0,
            }
        return cls.matches[room_name]

    @classmethod
    def assign_player(cls, room_name, channel_name):
        match = cls.create_match(room_name)

        if match['player1'] is None:
            match['player1'] = channel_name
            return 'paddle1'
        elif match['player2'] is None:
            match['player2'] = channel_name
            return 'paddle2'
        else:
            return None  # Room is full

    @classmethod
    def remove_player(cls, room_name, channel_name):
        match = cls.matches.get(room_name)

        if match:
            if match['player1'] == channel_name:
                match['player1'] = None
            elif match['player2'] == channel_name:
                match['player2'] = None

            # Optionally: Clear the match when both players leave
            if match['player1'] is None and match['player2'] is None:
                del cls.matches[room_name]

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_mode = self.scope['url_route']['kwargs']['game_mode']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'pong_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        self.match = MatchManager.create_match(self.room_name)
        self.player = MatchManager.assign_player(self.room_name, self.channel_name)
        self.id = MatchManager.assign_player_id()
        print(f"Match: {self.match}")  # Debugging line
        print(f"Player: {self.player}")  # Debugging line
        print(f"Game Mode: {self.game_mode}")  # Debugging line

        if (self.game_mode == "pvp"):
            await self.pvp_mode()
        elif (self.game_mode == "pve"):
            await self.pve_mode()
        elif (self.game_mode == "tournament"):
            await self.tournament_mode()

    async def disconnect(self, close_code):
        # Remove player from the room in RoomManager
        MatchManager.remove_player(self.room_name, self.channel_name)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if self.match['player1'] == None or self.match['player1'] == None:
            # If there are fewer than 2 players, end the game
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'end_game',
                    'message': 'A Player has disconnected, Game over!',
                }
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        paddle = data.get('paddle')
        velocity = data.get('velocity')

        # Update the paddle's velocity
        if paddle == 'paddle1':
            self.match['paddle1'].velocity = velocity
        elif paddle == 'paddle2':
            self.match['paddle2'].velocity = velocity

        message = data.get('message')
        if message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message': f'Player {self.id}: {message}'
                })

    async def pvp_mode(self):
        print("ENTERED PVP MODE FUNCTION")
        if self.player is None:
            await self.close()
        else:
            await self.send(text_data=json.dumps({
                'type': 'player_assignment',
                'player': self.player,
            }))
        if (self.match['player1'] != None and self.match['player2'] != None):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game',
                    'message': 'channel_layer.group_send: start_game',
                })
            asyncio.create_task(self.game_loop())

    async def pve_mode(self):
        print("ENTERED PVE MODE FUNCTION")
        await self.send(text_data=json.dumps({
        'type': 'player_assignment',
        'player': self.player,
        }))
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'start_game',
            'message': 'channel_layer.group_send: start_game',
        })
        asyncio.create_task(self.game_loop())

    async def tournament_mode(self):
        print("ENTERED TOURNAMENT MODE FUNCTION")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'Player {self.id} has joined the chat',
            }
        )

    async def start_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'start_game',
            'message': event['message'],
            'gameHeight': gameHeight,
            'gameWidth': gameWidth,
            'paddle1': self.match['paddle1'].serialize(),
            'paddle2': self.match['paddle2'].serialize(),
            'ball': self.match['ball'].serialize(),
        }))
        for i in range(3, 0, -1):
            await self.send(text_data=json.dumps({
                'type': 'countdown_game',
                'message': i,
            }))
            await asyncio.sleep(1)

    async def game_loop(self):
        await asyncio.sleep(4)
        while True:
            # Update game state
            self.match['ball'].move()
            self.match['paddle1'].move()
            self.match['paddle2'].move()

            # Check for scoring
            if self.match['ball'].x <= 0:
                self.match['score2'] += 1
                self.reset_ball()
            elif self.match['ball'].x >= gameWidth:
                self.match['score1'] += 1
                self.reset_ball()

            self.match['ball'].check_collision(self.match['paddle1'], self.match['paddle2'])

            # Broadcast game state to clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_game_state',
                    'paddle1': self.match['paddle1'].serialize(),
                    'paddle2': self.match['paddle2'].serialize(),
                    'ball': self.match['ball'].serialize(),
                    'score1': self.match['score1'],
                    'score2': self.match['score2'],
                }
            )

            # End the game if a player reaches a score of 5
            if self.match['score1'] >= 5 or self.match['score2'] >= 5:
                winner = 'player1' if self.match['score1'] >= 5 else 'player2'
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'end_game',
                        'message': f'{winner} wins! Game over!',
                    }
                )
                break  # Exit the game loop

            await asyncio.sleep(1/60)  # Run at ~60 FPS

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
        # Send game end message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'end_game',
            'message': event['message'],
        }))
        await self.close()  # Close the WebSocket connection

    def reset_ball(self):
        # Reset the ball to the center of the field
        self.match['ball'].x = gameWidth / 2
        self.match['ball'].y = gameHeight / 2
        self.match['ball'].x_direction *= -1  # Change direction after score
        self.match['ball'].speed = self.match['ball'].oriSpeed

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))


class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0

    def move(self):
        self.y += self.velocity
        # Keep paddle within bounds
        if self.y < 0:
            self.y = 0
        if self.y > gameHeight - self.height:
            self.y = gameHeight - self.height

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
        self.x_direction = 1
        self.y_direction = 1

    def move(self):
        self.x += self.speed * self.x_direction
        self.y += self.speed * self.y_direction

    def check_collision(self, paddle1, paddle2):
        # Y-axis collision
        if self.y <= 0 or self.y >= gameHeight - self.radius:
            self.y_direction *= -1

        # Paddle collision
        if (self.x <= paddle1.x + paddle1.width and 
            paddle1.y <= self.y <= paddle1.y + paddle1.height):
            self.x_direction = 1

        if (self.x >= paddle2.x - self.radius and 
            paddle2.y <= self.y <= paddle2.y + paddle2.height):
            self.x_direction = -1

            # Optionally, adjust speed slightly, but cap it
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
    
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('matchmaking', self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'join_queue':
            player_id = data.get('player_id')
            await self.join_queue(player_id)
    
    async def join_queue(self, player_id):
        player = await self.get_player(player_id)
        if player:
            await self.channel_layer.group_add('matchmaking', self.channel_name)
            await self.match_player(player)

    async def get_player(self, player_id):
        return await database_sync_to_async(Player.objects.get)(id=player_id)

    async def match_player(self, player):
        elo_range = 100
        max_elo_range = 200
        wait_time = 0

        while True:
            min_elo = player.elo_rating - elo_range
            max_elo = player.elo_rating + elo_range

            potential_opponents = await database_sync_to_async(Player.objects.filter)(
                elo_rating__gte=min_elo,
                elo_rating__lte=max_elo,
                channel_name__in=await self.get_waiting_players()
            ).exclude(id=player.id)

            if potential_opponents.exists():
                opponent = potential_opponents.first()
                await self.start_match(player, opponent)
                await self.channel_layer.group_discard('matchmaking', self.channel_name)
                break

            await asyncio.sleep(2)
            wait_time += 2
            elo_range = min(elo_range + 10, max_elo_range)

    async def get_waiting_players(self):
        group_channels = await self.channel_layer.group_channels("matchmaking")
        return [channel_name.split(".")[-1] for channel_name in group_channels]

    async def start_match(self, player, opponent):
        # WXR TODO: Logic to start the match
        pass

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
