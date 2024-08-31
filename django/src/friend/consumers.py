from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import json

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
        

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = 'online_users'

        # Add user to the "online_users" group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Mark this user as online in the cache
        cache.set(f"user_{self.user.id}_online", True)

        # Accept the WebSocket connection
        await self.accept()
        await self.send_initial_online_status()

        # Notify the group that a new user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'status': True  # Online
            }
        )

    async def disconnect(self, close_code):
        # Remove user from the "online_users" group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Mark this user as offline in the cache
        cache.delete(f"user_{self.user.id}_online")

        # Notify the group that the user is offline
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'status': False  # Offline
            }
        )
        
    async def send_initial_online_status(self):
        friends = self.user.friends.filter(deleted=False)
        online_friends = [friend_id for friend_id in friends if cache.get(f"user_{friend_id}_online")]
        initial_status = [{'user_id': friend_id, 'status': True} for friend_id in online_friends]
        await self.send(text_data=json.dumps({
            'initial_status': initial_status
        }))
