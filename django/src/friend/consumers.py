import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FriendRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"friend_requests_{self.user.id}"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def friend_request_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event["message"]))