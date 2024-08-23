import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

gameHeight = 500
gameWidth = 800

class GameManager:
    games = {}

    @classmethod
    def get_game(cls, room_name):
        if room_name not in cls.games:
            cls.games[room_name] = {
                'paddle1': Paddle(20, 200, 10, 100),
                'paddle2': Paddle(gameWidth - 30, 200, 10, 100),
                'ball': Ball(400, 250, 8, 5),
                'score1': 0,
                'score2': 0,
            }
        return cls.games[room_name]

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Track the number of players
        if not hasattr(self.channel_layer, 'players'):
            self.channel_layer.players = {}

        # Assign the player to paddle1 or paddle2
        if 'player1' not in self.channel_layer.players:
            self.channel_layer.players['player1'] = self.channel_name
            self.player = 'paddle1'
        elif 'player2' not in self.channel_layer.players:
            self.channel_layer.players['player2'] = self.channel_name
            self.player = 'paddle2'
        else:
            # More than two players connecting, you can handle this case if needed
            await self.close()

        # Send the player assignment to the client
        await self.send(text_data=json.dumps({
            'type': 'player_assignment',
            'player': self.player,
        }))

        game_state = GameManager.get_game(self.room_name)
        self.paddle1 = game_state['paddle1']
        self.paddle2 = game_state['paddle2']
        self.ball = game_state['ball']
        self.score1 = game_state['score1']
        self.score2 = game_state['score2']

        # Start the game loop when two player connect
        if len(self.channel_layer.players) == 2:
            print("Two Players are connected!")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game',
                    'message': 'Two Players are connected, Game Start!',
                }
            )
            asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Remove the player from the players list
        if self.player == 'paddle1':
            del self.channel_layer.players['player1']
        elif self.player == 'paddle2':
            del self.channel_layer.players['player2']

    async def receive(self, text_data):
        data = json.loads(text_data)
        paddle = data.get('paddle')
        velocity = data.get('velocity')

        # Update the paddle's velocity
        if paddle == 'paddle1':
            self.paddle1.velocity = velocity
        elif paddle == 'paddle2':
            self.paddle2.velocity = velocity

    async def start_game(self, event):
        # Send the matchmaking message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'start_game',
            'message': event['message'],
        }))

    async def game_loop(self):
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

    def reset_ball(self):
        # Reset the ball to the center of the field
        self.ball.x = gameWidth / 2
        self.ball.y = gameHeight / 2
        self.ball.x_direction *= -1  # Change direction after score
        self.ball.speed = self.ball.oriSpeed

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
