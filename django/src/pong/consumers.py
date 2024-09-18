import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import GameRoom

gameHeight = 500
gameWidth = 800

class RoomManager:
    rooms = {}  # A dictionary to map room names to their respective managers

    @classmethod
    def get_match_manager(cls, room_name):
        if room_name not in cls.rooms:
            cls.rooms[room_name] = MatchManager()
        return cls.rooms[room_name]

    @classmethod
    def remove_room(cls, room_name):
        if room_name in cls.rooms:
            del cls.rooms[room_name]

class MatchManager:
    def __init__(self):
        self.players = [] # List of channel_names (WebSocket connections)
        self.matches = []
        self.match_index = 0

        self.paddle1 = Paddle(20, 200, 10, 100)
        self.paddle2 = Paddle(gameWidth - 30, 200, 10, 100)
        self.ball = Ball(400, 250, 8, 5)
        self.score1 = 0
        self.score2 = 0

    def add_player(self, channel_name):
        self.players.append(channel_name)

    def generate_matches(self):
        if len(self.players) % 2 != 0:
            raise ValueError("Tournament requires an even number of players")

        # Shuffle players and pair them for the matches
        random.shuffle(self.players)
        self.matches = [(self.players[i], self.players[i+1]) for i in range(0, len(self.players), 2)]

    def get_next_match(self):
        if self.match_index < len(self.matches):
            match = self.matches[self.match_index]
            self.match_index += 1
            return match
        return None  # No more matches

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_mode = self.scope['url_route']['kwargs']['game_mode']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'pong_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        self.manager = RoomManager.get_match_manager(self.room_name)
        self.player = self.manager.add_player(self.channel_name)

        if (self.game_mode == "pvp"):
            await self.pvp_mode()
        elif (self.game_mode == "pve"):
            await self.pve_mode()
        elif (self.game_mode == "tournament"):
            await self.tournament_mode()

    async def disconnect(self, close_code):
        try:
            game_room = await sync_to_async(GameRoom.objects.get)(room_name=self.room_name)
            await sync_to_async(game_room.delete)()
        except GameRoom.DoesNotExist:
            pass  # Room already deleted or not found

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        paddle = data.get('paddle')
        velocity = data.get('velocity')

        # Update the paddle's velocity
        if paddle == 'paddle1':
            self.manager.paddle1.velocity = velocity
        elif paddle == 'paddle2':
            self.manager.paddle2.velocity = velocity

    async def pvp_mode(self):
        if len(self.manager.players) == 2:
            self.manager.generate_matches()
            self.player1, self.player2 = self.manager.get_next_match()

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
        if len(self.manager.players) == 1:
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

    async def tournament_mode(self):
        print("ENTERED TOURNAMENT MODE FUNCTION")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'Player {self.id} has joined the chat',
            }
        )


    async def paddle_assignment(self, event):
        await self.send(text_data=json.dumps({
            'type': 'paddle_assignment',
            'message': event['message'],
            'paddle': event['paddle'],
        }))

    async def start_game(self, event):
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

            # Check if a player disconnected
            if self.player1 == None or self.player2 == None:
                winner = 'Player 1' if self.player2 == None else 'Player 2'
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'end_game',
                        'message': f'{winner} wins!\nBecause other player disconnected!',
                    }
                )
                break  # Exit the game loop

            winningScore = 10

            # End the game if a player reaches a score of winningScore
            if self.manager.score1 >= winningScore or self.manager.score2 >= winningScore:
                winner = 'Player 1' if self.manager.score1 >= winningScore else 'Player 2'
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'end_game',
                        'message': f'{winner} wins!',
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

    def reset_ball(self):
        # self.match['ball'].x = gameWidth / 2
        # self.match['ball'].y = gameHeight / 2
        # self.match['ball'].speed = self.match['ball'].oriSpeed
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
