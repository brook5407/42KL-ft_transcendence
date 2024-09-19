from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import ChatRoom, ChatMessage
from pong.models import MatchInvitation
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

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data['type']
        if type == 'chat_message':
            await self.handle_message(data)
        elif type == 'pong_invitation':
            await self.handle_pong_invitation(data)
        elif type == 'pong_invitation_accept_acknowledgement':
            await self.handle_pong_invitation_accept_acknowledgement(data)
            
    async def handle_pong_invitation_accept_acknowledgement(self, data):
        room_id = data['room_id']
        room = await self.get_room(room_id)
        match_invitation_id = data['match_invitation_id']
        user_profile = await sync_to_async(lambda: self.user.profile)()
        other_member = await self.get_other_member(room)
        
        await self.accept_pong_invitation(match_invitation_id)
        match_id = await self.create_match(match_invitation_id)
        
        for group in [f"private_chats_{self.user.id}", f"private_chats_{other_member.id}"]:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'pong_invitation_message',
                    'action': 'accept_acknowledgement',
                    'message': f'Pong invitation accept acknowledged',
                    'sender': {
                        'id': self.user.id,
                        'username': self.user.username,
                        'email': self.user.email,
                        'profile': {
                            'nickname': user_profile.nickname,
                            'bio': user_profile.bio,
                            'avatar': user_profile.avatar.url,
                        }
                    },
                    'match_invitation_id': match_invitation_id,
                    'match_id': match_id,
                    'room_id': room_id,
                    'room_name': room.name,
                    'created_at': timezone.now().isoformat(),
                }
            )
            
    @database_sync_to_async
    def create_match(self, match_invitation_id):
        match_invitation = MatchInvitation.objects.get(id=match_invitation_id)
        match = match_invitation.create_match()
        return match.id
    
    @database_sync_to_async
    def accept_pong_invitation(self, match_invitation_id):
        match_invitation = MatchInvitation.objects.get(id=match_invitation_id)
        if match_invitation.status == 'W':
            match_invitation.accept()
        
    @database_sync_to_async
    def reject_pong_invitation(self, match_invitation_id):
        match_invitation = MatchInvitation.objects.get(id=match_invitation_id)
        if match_invitation.status == 'W':
            match_invitation.reject()
            
    async def handle_pong_invitation(self, data):
        accept = data['accept']
        room_id = data['room_id']
        match_invitation_id = data['match_invitation_id']
        
        room = await self.get_room(room_id)
        if room.is_group_chat:
            return
        user_profile = await sync_to_async(lambda: self.user.profile)()
        other_member = await self.get_other_member(room)
        
        if not accept:
            await self.reject_pong_invitation(match_invitation_id)
        
        await self.channel_layer.group_send(
            f"private_chats_{other_member.id}",
            {
                'type': 'pong_invitation_message',
                'action': 'accept' if accept else 'reject',
                'message': f'Pong invitation {"accepted" if accept else "rejected"}',
                'sender': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'email': self.user.email,
                    'profile': {
                        'nickname': user_profile.nickname,
                        'bio': user_profile.bio,
                        'avatar': user_profile.avatar.url,
                    }
                },
                'match_invitation_id': match_invitation_id,
                'room_id': room_id,
                'room_name': room.name,
                'created_at': timezone.now().isoformat(),
            }
        )
    
    async def handle_message(self, data):
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
                        'id': self.user.id,
                        'username': self.user.username,
                        'email': self.user.email,
                        'profile': {
                            'nickname': user_profile.nickname,
                            'bio': user_profile.bio,
                            'avatar': user_profile.avatar.url,
                        }
                    },
                    'room_name': room.name,
                    'cover_image': room.cover_image.url,
                    'room_id': room_id,
                    'created_at': timezone.now().isoformat(),
                }
            )
            chat_message = await self.create_chat_message(message, room)
        else:
            other_member = await self.get_other_member(room)
            if not other_member:
                await self.send(text_data=json.dumps({
                    'error': 'user_not_found',
                    'message': 'User is no longer available'
                }))
                return
            if not await sync_to_async(lambda: self.user.is_friend(other_member))():
                await self.send(text_data=json.dumps({
                    'error': 'not_friend',
                    'message': 'You are not friend with this user'
                }))
                return
            elif await sync_to_async(lambda: self.user.is_blocked(other_member))():
                await self.send(text_data=json.dumps({
                    'error': 'blocked',
                    'message': 'You have blocked the user'
                }))
                return
            elif await sync_to_async(lambda: other_member.is_blocked(self.user))():
                await self.send(text_data=json.dumps({
                    'error': 'blocked_by_other',
                    'message': 'The user has blocked you'
                }))
                return

            chat_message = await self.create_chat_message(message, room)
            for group in [f"private_chats_{self.user.id}", f"private_chats_{other_member.id}"]:
                await self.channel_layer.group_send(
                    group,
                    {
                        'type': 'private_chat_message',
                        'message': message,
                        'sender': {
                           'id': self.user.id,
                            'username': self.user.username,
                            'email': self.user.email,
                            'profile': {
                                'nickname': user_profile.nickname,
                                'bio': user_profile.bio,
                                'avatar': user_profile.avatar.url,
                            }
                        },
                        'match_invitation_id': chat_message.match_invitation.id if chat_message.match_invitation else None,
                        'room_name': room.name,
                        'room_id': room_id,
                        'created_at': timezone.now().isoformat(),
                    }
                )
        
    @database_sync_to_async
    def get_room(self, room_id):
        return ChatRoom.objects.get(id=room_id)

    @database_sync_to_async
    def create_chat_message(self, message, room):
        if message.startswith('/invite'):
            match_invitation = MatchInvitation.objects.create(sender=self.user, receiver=room.members.exclude(id=self.user.id).first())
            return ChatMessage.objects.create(message=message, sender=self.user, room=room, match_invitation=match_invitation)
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
        created_at = event['created_at'] or timezone.now().isoformat()

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'group_chat_message',
            'message': message,
            'sender': sender,
            'room_id': room_id,
            'room_name': room_name,
            'cover_image': cover_image,
            'created_at': created_at,
        }))

    # Handling private chat notifications
    async def private_chat_message(self, event):
        message = event['message']
        sender = event['sender']
        match_invitation_id = event.get('match_invitation_id', None)
        room_id = event['room_id']
        room_name = event['room_name']
        created_at = event['created_at'] or timezone.now().isoformat()

        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'private_chat_message',
            'message': message,
            'sender': sender,
            'match_invitation_id': match_invitation_id,
            'room_id': room_id,
            'room_name': room_name,
            'created_at': created_at,
        }))
        
    async def pong_invitation_message(self, event):
        action = event['action']
        message = event['message']
        sender = event['sender']
        match_invitation_id = event.get('match_invitation_id', None)
        match_id = event.get('match_id', None)
        room_id = event['room_id']
        room_name = event['room_name']
        created_at = event['created_at'] or timezone.now().isoformat()

        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'pong_invitation_message',
            'action': action,
            'message': message,
            'sender': sender,
            'match_invitation_id': match_invitation_id,
            'match_id': match_id,
            'room_id': room_id,
            'room_name': room_name,
            'created_at': created_at,
        }))
