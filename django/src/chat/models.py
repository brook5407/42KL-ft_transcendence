from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from base.models import BaseModel
from pong.models import MatchInvitation
import uuid


User = get_user_model()

class ChatRoom(BaseModel):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, blank=True, related_name='chatroom_members')
    is_public = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='chatroom_covers/', null=True)
    is_group_chat = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)


    def get_last_message(self):
        return self.chat_messages.order_by('-created_at').first()

    @staticmethod
    def get_private_chats(user):
        return ChatRoom.objects.filter(members=user, is_public=False)
    
    @staticmethod
    def get_private_chat_roomname(user1, user2):
        member_names = sorted([user1.username, user2.username])
        roomname = "-".join(member_names)
        return roomname

    def get_room_name(self, user):
        if self.is_group_chat:
            return self.name
        other_member = self.members.exclude(id=user.id).first()
        if other_member:
            return other_member.username
        return 'default_room_name'


class ChatMessage(BaseModel):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message = models.TextField()  # for game invitation, message will have a /invite prefix
    match_invitation = models.OneToOneField(MatchInvitation, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(ChatRoom, related_name='chat_messages', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['room']),
            models.Index(fields=['sender']),
        ]

    def __str__(self):
        sender_name = self.sender.username if self.sender else "No Sender"
        return f"Message from {sender_name} in room {self.room.name} at {self.created_at}: {self.message}"


class ActiveChatRoom(BaseModel):
    # For chat list display (last message and unread count for a specific user)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    last_message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, null=True, blank=True)
    unread_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['room']),
        ]

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"
