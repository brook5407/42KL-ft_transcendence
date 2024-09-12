from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from .models import ChatRoom
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # Connect user to all group chats
            await self.add_to_group_chats()

            # Connect to private notification group
            await self.channel_layer.group_add(
                f"private_chats_{self.user.id}",
                self.channel_name
            )
            
            await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Disconnect from group chats
            await self.remove_from_group_chats()

            # Disconnect from private notification group
            await self.channel_layer.group_discard(
                f"private_chats_{self.user.id}",
                self.channel_name
            )

    async def add_to_group_chats(self):
        # Fetch all group chats the user is part of
        group_chats = await self.get_group_chat_rooms()
        for room in group_chats:
            await self.channel_layer.group_add(
                room.id,
                self.channel_name
            )

    async def remove_from_group_chats(self):
        # Fetch all group chats the user is part of
        group_chats = await self.get_group_chat_rooms()
        for room in group_chats:
            await self.channel_layer.group_discard(
                room.id,
                self.channel_name
            )

    @database_sync_to_async
    def get_group_chat_rooms(self):
        try:
            return list(ChatRoom.objects.filter(Q(members=self.user, is_group_chat=True) | Q(is_public=True)))
        except ChatRoom.DoesNotExist:
            return []

    # Handling incoming messages (for group chat)
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        room_id = data['room_id']
        
        # Send message to the room group
        await self.channel_layer.group_send(
            room_id,
            {
                'type': 'group_chat_message',
                'message': message,
                'user': self.user.username,
                'room_id': room_id
            }
        )

    async def group_chat_message(self, event):
        print("group chat message sending....")
        message = event['message']
        user = event['user']
        room_id = event['room_id']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'room_id': room_id
        }))

    # Handling private chat notifications
    async def private_chat_message(self, event):
        message = event['message']
        sender = event['sender']
        room_id = event['room_id']

        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'private_chat_message',
            'message': message,
            'sender': sender,
            'room_id': room_id,
        }))