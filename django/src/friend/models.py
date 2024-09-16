from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from django.forms import ValidationError
from base.models import BaseModel


User = get_user_model()

# Create your models here.
class UserRelation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_relations")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_relations", default=None)
    blocked = models.BooleanField(default=False)
    blocked_at = models.DateTimeField(auto_now=False, null=True)
    
    class Meta:
        unique_together = ['user', 'friend']

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
    
    def delete_friend(self):
        friend_user_relation = UserRelation.objects.get(user=self.friend, friend=self.user)
        friend_user_relation.delete()
        self.delete()
        
    def block(self):
        if self.blocked:
            raise ValidationError("User is already blocked.")
        self.blocked = True
        self.blocked_at = timezone.now()
        self.save()
    
    def unblock(self):
        if not self.blocked:
            raise ValidationError("User is not blocked.")
        self.blocked = False
        self.blocked_at = None
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

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"
    
    def accept(self, current_user):
        if current_user == self.sender:
            raise ValidationError("You cannot accept your own request.")
        elif current_user != self.receiver:
            raise ValidationError("You cannot accept a request that is not addressed to you.")
        self.status = self.Status.ACCEPTED
        self.save()
        
    def reject(self, current_user):
        if current_user == self.sender:
            raise ValidationError("You cannot reject your own request.")
        elif current_user != self.receiver:
            raise ValidationError("You cannot accept a request that is not addressed to you.")
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
    user_relations = UserRelation.objects.filter(Q(user=self))
    friend_ids = user_relations.values_list('friend_id', flat=True)
    friends = User.objects.filter(id__in=friend_ids)
    return friends

def is_friend(self, user):
    return UserRelation.objects.filter(Q(user=self) & Q(friend=user)).exists()

def is_blocked(self, user):
    return UserRelation.objects.filter(Q(user=self) & Q(friend=user) & Q(blocked=True)).exists()

User.add_to_class('friends', property(get_friends))
User.add_to_class('is_friend', is_friend)
User.add_to_class('is_blocked', is_blocked)