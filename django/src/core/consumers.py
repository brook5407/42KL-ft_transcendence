import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'

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
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',
                'paddle1': data.get('paddle1'),
                'paddle2': data.get('paddle2'),
                'ball': data.get('ball')
            }
        )

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'paddle1': event.get('paddle1'),
            'paddle2': event.get('paddle2'),
            'ball': event.get('ball')
        }))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'You are now connected!'
        }))