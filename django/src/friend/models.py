from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from base.models import BaseModel

# Create your models here.
class UserRelation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_relations")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_relations", default=None)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=False, null=True)
    blocked = models.BooleanField(default=False)
    blocked_at = models.DateTimeField(auto_now=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'friend']

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
    
    def delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
        
    def block(self):
        self.blocked = True
        self.blocked_at = timezone.now()
        self.save()
    
    def unblock(self):
        self.blocked = False
        self.save()


class FriendRequest(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        ACCEPTED = 'A', 'Accepted'
        REJECTED = 'R', 'Rejected'

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_requests", default=None)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    receiver_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"
    
    def accept(self, current_user):
        if current_user == self.sender:
            raise ValueError("You cannot accept your own request.")
        elif current_user != self.receiver:
            raise ValueError("You cannot accept a request that is not addressed to you.")
        self.status = self.Status.ACCEPTED
        self.save()
        
    def reject(self, current_user):
        if current_user == self.sender:
            raise ValueError("You cannot reject your own request.")
        elif current_user != self.receiver:
            raise ValueError("You cannot accept a request that is not addressed to you.")
        self.status = self.Status.REJECTED
        self.save()
        
    def notify_friend_request_update(self):
        channel_layer = get_channel_layer()
        receiver_group_name = f"friend_requests_{self.receiver.id}"
        sender_group_name = f"friend_requests_{self.sender.id}"
        message = {
            "type": "friend_request_update",
                "message": {
                    "id": self.id,
                    "sender": self.sender.username,
                    "receiver": self.receiver.username,
                    "status": self.status,
                },
        }
        async_to_sync(channel_layer.group_send)(
            receiver_group_name,
            message
        )
        async_to_sync(channel_layer.group_send)(
            sender_group_name,
            message
        )


def get_friends(self):
    user_relations = UserRelation.objects.filter(Q(user=self) | Q(friend=self))
    friends = user_relations.filter(deleted=False, blocked=False)
    return friends

User.add_to_class('friends', property(get_friends))