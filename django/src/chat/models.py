from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from base.models import BaseModel
import uuid



User = get_user_model()

class ChatRoom(BaseModel):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, blank=True, related_name='chatroom_members')
    is_public = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='chatroom_covers/', null=True, blank=True)
    is_group_chat = models.BooleanField(default=False)
    # messages = models.ForeignKey('ChatMessage', related_name='chatroom_messages', on_delete=models.CASCADE)
    messages = models.ManyToManyField('ChatMessage', related_name='chatroom_messages')

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.id = str(uuid.uuid4())
    #     if self.members.count() == 2:
    #         member_names = sorted([str(member.username) for member in self.members.all()])
    #         self.name = "-".join(member_names)
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)


    def get_last_message(self):
        return self.chat_messages.order_by('-timestamp').first()

    @staticmethod
    def get_private_chats(user):
        return ChatRoom.objects.filter(members=user, is_public=False)
    
    @staticmethod
    def get_private_chat_roomname(user1, user2):
        member_names = sorted([str(member.username) for member in [user1, user2]])
        roomname = "-".join(member_names)
        # roomname = "-2.join(member_names)
        return roomname

    def get_room_name(self, user):
        if self.is_group_chat:
            return self.name
        other_member = self.members.exclude(id=user.id).first()
        if other_member:
            return other_member.username
        return 'default_room_name'

    def print_chat_history(self):
        messages = self.chat_messages.order_by('timestamp')
        for message in messages:
            sender = message.sender.username
            receiver = message.receiver.username if message.receiver else "No Receiver"
            timestamp = message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] {sender} to {receiver}: {message.message}")

    # def get_room_name(self, user):
    #     if self.is_group_chat:
    #         return self.name
    #     return self.members.exclude(id=user.id).first().username

class ChatMessage(BaseModel):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()  # for game invitation, message will have a /invite prefix
    room = models.ForeignKey(ChatRoom, related_name='chat_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        receiver_name = self.receiver.username if self.receiver else "No Receiver"
        sender_name = self.sender.username if self.sender else "No Sender"
        return f"Message from {sender_name} to {receiver_name} in room {self.room.name} at {self.timestamp}: {self.message}"
    # Optional: Custom method to print a full message
    def print_message(self):
        if self.receiver:
            print(f"Message from {self.sender.username} to {self.receiver.username}: {self.message}")
        else:
            print(f"Message from {self.sender.username} to None: {self.message}")
        # print(f"Message from {self.sender.username} to {self.receiver.username if self.receiver else 'None'}: {self.message}")
