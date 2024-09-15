import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import GameRoom

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

            # AI Paddle follows the ball
            if (self.game_mode == "pve"):
                self.match['paddle2'].follow_ball(self.match['ball'])

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
        try:
            game_room = GameRoom.objects.get(room_name=self.room_name)
            game_room.delete()  # Delete the room when the game is over or a player disconnects
        except GameRoom.DoesNotExist:
            pass  # Room already deleted or not found

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # await self.close()  # Close the WebSocket connection

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

# class TournamentConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'tournament_{self.room_name}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data['type']

#         if message_type == 'join_room':
#             await self.join_room(data['player_id'])
#         elif message_type == 'match_result':
#             await self.update_match_result(data['match_id'], data['winner_id'])

#     async def join_room(self, player_id):
#         room = await database_sync_to_async(Room.objects.get)(name=self.room_name)
#         player = await database_sync_to_async(Player.objects.get)(id=player_id)
#         await database_sync_to_async(room.players.add)(player)

#         if await database_sync_to_async(room.players.count)() == 8:
#             await self.start_tournament(room)

#     async def start_tournament(self, room):
#         players = await database_sync_to_async(list)(room.players.all())
#         await database_sync_to_async(create_matches)(players, "Quarter Finals")

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'tournament_message',
#                 'message': 'Tournament started'
#             }
#         )

#     async def update_match_result(self, match_id, winner_id):
#         match = await database_sync_to_async(Match.objects.get)(id=match_id)
#         winner = await database_sync_to_async(Player.objects.get)(id=winner_id)
#         await database_sync_to_async(setattr)(match, 'winner', winner)
#         await database_sync_to_async(match.save)()

#         # Check if all matches in the current round are complete
#         round_complete = await self.check_round_complete(match.round)
#         if round_complete:
#             await self.progress_to_next_round(match.round)

#     async def check_round_complete(self, round_name):
#         incomplete_matches = await database_sync_to_async(Match.objects.filter)(
#             tournament__room__name=self.room_name,
#             round=round_name,
#             winner__isnull=True
#         ).count()
#         return incomplete_matches == 0

#     async def progress_to_next_round(self, current_round):
#         if current_round == "Quarter Finals":
#             next_round = "Semi Finals"
#         elif current_round == "Semi Finals":
#             next_round = "Final"
#         else:
#             return

#         winners = await database_sync_to_async(list)(
#             Match.objects.filter(
#                 tournament__room__name=self.room_name,
#                 round=current_round
#             ).values_list('winner', flat=True)
#         )
#         await database_sync_to_async(create_matches)(winners, next_round)

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'tournament_message',
#                 'message': f'{next_round} started'
#             }
#         )

#     async def tournament_message(self, event):
#         message = event['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))



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
        self.x_direction = 1
        self.y_direction = 1

    def move(self):
        self.x += self.speed * self.x_direction
        self.y += self.speed * self.y_direction

    # def check_collision(self, paddle1, paddle2):
    #     # Y-axis collision with the top and bottom of the game area
    #     if self.y <= 0 or self.y >= gameHeight - self.radius:
    #         self.y_direction *= -1

    #     # Paddle collision
    #     if (self.x <= paddle1.x + paddle1.width and 
    #         paddle1.y <= self.y <= paddle1.y + paddle1.height):
    #         self.x_direction = 1

    #     if (self.x >= paddle2.x - self.radius and 
    #         paddle2.y <= self.y <= paddle2.y + paddle2.height):
    #         self.x_direction = -1

    #         # Optionally, adjust speed slightly, but cap it
    #         self.speed = min(self.speed + 1, 15)

    def check_collision(self, paddle1, paddle2):
        # Y-axis collision with the top and bottom of the game area
        if (self.y - self.radius) <= 0 or (self.y + self.radius) >= gameHeight:
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
