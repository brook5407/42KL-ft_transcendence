from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest, UserRelation

@receiver(post_save, sender=FriendRequest)
def create_user_relation(sender, instance, **kwargs):
    if instance.status == FriendRequest.Status.ACCEPTED:
        UserRelation.objects.update_or_create(
            user=instance.sender,
            friend=instance.receiver,
            defaults={'deleted': False, 'deleted_at': None}
        )
        UserRelation.objects.update_or_create(
            user=instance.receiver,
            friend=instance.sender,
            defaults={'deleted': False, 'deleted_at': None}
        )
        
@receiver(post_save, sender=FriendRequest)
def trigger_notify_friend_request_update(sender, instance, **kwargs):
    instance.notify_friend_request_update()