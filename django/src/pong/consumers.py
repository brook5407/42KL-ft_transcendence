import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
# from .models import Tournament, Room, Match

gameHeight = 500
gameWidth = 800

class RoomsManager:
    rooms = {}

    @classmethod
    def get_room(cls, room_name):
        if room_name not in cls.rooms:
            cls.rooms[room_name] = {
                'players': {},
                'paddle1': Paddle(20, 200, 10, 100),
                'paddle2': Paddle(gameWidth - 30, 200, 10, 100),
                'ball': Ball(400, 250, 8, 5),
                'score1': 0,
                'score2': 0,
            }
        return cls.rooms[room_name]

    @classmethod
    def assign_player(cls, room_name, channel_name):
        room = cls.get_room(room_name)
        if 'player1' not in room['players']:
            room['players']['player1'] = channel_name
            return 'paddle1'
        elif 'player2' not in room['players']:
            room['players']['player2'] = channel_name
            return 'paddle2'
        else:
            return None  # Room is full
        
    @classmethod
    def remove_player(cls, room_name, channel_name):
        room = cls.get_room(room_name)
        if 'player1' in room['players']:
            room['players']['player1'] = channel_name
            del room['players']['player1']
        elif 'player2' in room['players']:
            room['players']['player2'] = channel_name
            del room['players']['player2']
        else:
            return None  # Room is empty

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_mode = self.scope['url_route']['kwargs']['game_mode']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Assign the player using RoomsManager
        self.player = RoomsManager.assign_player(self.room_name, self.channel_name)

        if (self.game_mode == "pvp"):
            self.pvp_mode()
        elif (self.game_mode == "pve"):
            self.pve_mode()
        elif (self.game_mode == "tournament"):
            self.tournament_mode()

        if self.player is None:
            # Room is full, close the connection
            await self.close()
        else:
            # Send the player assignment to the client
            await self.send(text_data=json.dumps({
                'type': 'player_assignment',
                'player': self.player,
            }))

        game_state = RoomsManager.get_room(self.room_name)
        self.paddle1 = game_state['paddle1']
        self.paddle2 = game_state['paddle2']
        self.ball = game_state['ball']
        self.score1 = game_state['score1']
        self.score2 = game_state['score2']

        # Start the game and game loop
        if len(game_state['players']) == 2 or self.game_mode == "pve":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game',
                    'message': 'channel_layer.group_send: start_game',
                })
            asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        # Remove player from the room in RoomManager
        RoomsManager.remove_player(self.room_name, self.channel_name)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        game_state = RoomsManager.get_room(self.room_name)
        if len(game_state['players']) < 2:
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
            self.paddle1.velocity = velocity
        elif paddle == 'paddle2':
            self.paddle2.velocity = velocity

    async def pvp_mode(self):
        print("pvp")
    async def pve_mode(self):
        print("pve")
    async def tournament_mode(self):
        print("tournament")

    async def start_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'start_game',
            'message': event['message'],
            'gameHeight': gameHeight,
            'gameWidth': gameWidth,
            'paddle1': self.paddle1.serialize(),
            'paddle2': self.paddle2.serialize(),
            'ball': self.ball.serialize(),
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
            self.ball.move()
            self.paddle1.move()
            self.paddle2.move()

            # Check for scoring
            if self.ball.x <= 0:
                self.score2 += 1
                self.reset_ball()
            elif self.ball.x >= gameWidth:
                self.score1 += 1
                self.reset_ball()

            self.ball.check_collision(self.paddle1, self.paddle2)

            # Broadcast game state to clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_game_state',
                    'paddle1': self.paddle1.serialize(),
                    'paddle2': self.paddle2.serialize(),
                    'ball': self.ball.serialize(),
                    'score1': self.score1,
                    'score2': self.score2,
                }
            )

            # End the game if a player reaches a score of 5
            if self.score1 >= 5 or self.score2 >= 5:
                winner = 'player1' if self.score1 >= 5 else 'player2'
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
        self.ball.x = gameWidth / 2
        self.ball.y = gameHeight / 2
        self.ball.x_direction *= -1  # Change direction after score
        self.ball.speed = self.ball.oriSpeed

class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'tournament_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'join_room':
            await self.join_room(data['player_id'])
        elif message_type == 'match_result':
            await self.update_match_result(data['match_id'], data['winner_id'])

    async def join_room(self, player_id):
        room = await database_sync_to_async(Room.objects.get)(name=self.room_name)
        player = await database_sync_to_async(Player.objects.get)(id=player_id)
        await database_sync_to_async(room.players.add)(player)

        if await database_sync_to_async(room.players.count)() == 8:
            await self.start_tournament(room)

    async def start_tournament(self, room):
        players = await database_sync_to_async(list)(room.players.all())
        await database_sync_to_async(create_matches)(players, "Quarter Finals")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tournament_message',
                'message': 'Tournament started'
            }
        )

    async def update_match_result(self, match_id, winner_id):
        match = await database_sync_to_async(Match.objects.get)(id=match_id)
        winner = await database_sync_to_async(Player.objects.get)(id=winner_id)
        await database_sync_to_async(setattr)(match, 'winner', winner)
        await database_sync_to_async(match.save)()

        # Check if all matches in the current round are complete
        round_complete = await self.check_round_complete(match.round)
        if round_complete:
            await self.progress_to_next_round(match.round)

    async def check_round_complete(self, round_name):
        incomplete_matches = await database_sync_to_async(Match.objects.filter)(
            tournament__room__name=self.room_name,
            round=round_name,
            winner__isnull=True
        ).count()
        return incomplete_matches == 0

    async def progress_to_next_round(self, current_round):
        if current_round == "Quarter Finals":
            next_round = "Semi Finals"
        elif current_round == "Semi Finals":
            next_round = "Final"
        else:
            return

        winners = await database_sync_to_async(list)(
            Match.objects.filter(
                tournament__room__name=self.room_name,
                round=current_round
            ).values_list('winner', flat=True)
        )
        await database_sync_to_async(create_matches)(winners, next_round)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tournament_message',
                'message': f'{next_round} started'
            }
        )

    async def tournament_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
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
