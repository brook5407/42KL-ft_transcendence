from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from asgiref.sync import sync_to_async
from .models import ChatRoom, ChatMessage
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
        
        # Fetch the room
        room = await self.get_room(room_id)
        
        user_profile = await sync_to_async(lambda: self.user.profile)()
        
        # Check if the room is a group chat or private chat
        if room.is_group_chat:
            await self.channel_layer.group_send(
                room_id,
                {
                    'type': 'group_chat_message',
                    'message': message,
                    'sender': {
                        'username': self.user.username,
                        'nickname': user_profile.nickname,
                        'avatar': user_profile.avatar.url
                    },
                    'room_name': room.name,
                    'cover_image': room.cover_image.url,
                    'room_id': room_id,
                }
            )
        else:
            other_member = await self.get_other_member(room)
            await self.channel_layer.group_send(
                f"private_chats_{other_member.id}",
                {
                    'type': 'private_chat_message',
                    'message': message,
                    'sender': {
                        'username': self.user.username,
                        'nickname': user_profile.nickname,
                        'avatar': user_profile.avatar.url
                    },
                    'room_name': room.name,
                    'room_id': room_id
                }
            )
            
        # Create the chat message in the database
        chat_message = await self.create_chat_message(message, room)
        
    @database_sync_to_async
    def get_room(self, room_id):
        return ChatRoom.objects.get(id=room_id)

    @database_sync_to_async
    def create_chat_message(self, message, room):
        return ChatMessage.objects.create(message=message, sender=self.user, room=room)

    @database_sync_to_async
    def get_other_member(self, room):
        return room.members.exclude(id=self.user.id).first()

    async def group_chat_message(self, event):
        message = event['message']
        sender = event['sender']
        room_id = event['room_id']
        room_name = event['room_name']
        cover_image = event['cover_image']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'group_chat_message',
            'message': message,
            'sender': sender,
            'room_id': room_id,
            'room_name': room_name,
            'cover_image': cover_image,
        }))

    # Handling private chat notifications
    async def private_chat_message(self, event):
        message = event['message']
        sender = event['sender']
        room_id = event['room_id']
        room_name = event['room_name']

        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'private_chat_message',
            'message': message,
            'sender': sender,
            'room_id': room_id,
            'room_name': room_name,
        }))