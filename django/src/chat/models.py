from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

class ChatRoom(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, blank=True, related_name='chatroom_members')
    is_public = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='chatroom_covers/', null=True, blank=True)
    is_group_chat = models.BooleanField(default=False)
    messages = models.ManyToManyField('ChatMessage', related_name='chatroom_messages')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def get_last_message(self):
        return self.messages.order_by('-timestamp').first()

    @staticmethod
    def get_private_chats(user):
        return ChatRoom.objects.filter(members=user, is_public=False)

    def get_room_name(self, user):
        if self.is_group_chat:
            return self.name
        return self.members.exclude(id=user.id).first().username

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, default=1)
    message = models.TextField()  # for game invitation, message will have a /invite prefix
    room = models.ForeignKey(ChatRoom, related_name='chat_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} in room {self.room.name} at {self.timestamp}"

