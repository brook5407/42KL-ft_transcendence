from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest, UserRelation

@receiver(post_save, sender=FriendRequest)
def create_user_relation(sender, instance, **kwargs):
    if instance.status == FriendRequest.Status.ACCEPTED:
        UserRelation.objects.get_or_create(
            user=instance.sender,
            friend=instance.receiver
        )
        UserRelation.objects.get_or_create(
            user=instance.receiver,
            friend=instance.sender
        )
        
@receiver(post_save, sender=FriendRequest)
def trigger_notify_friend_request_update(sender, instance, **kwargs):
    instance.notify_friend_request_update()