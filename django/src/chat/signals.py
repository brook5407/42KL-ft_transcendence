# signals.py
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import ChatMessage, ChatRoom
from friend.models import UserRelation as Friend


@receiver(post_save, sender=ChatMessage)
def limit_public_chat_messages(sender, instance, **kwargs):
    room = instance.room
    if room is None:
        return
    if not room.is_public:
        return
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
    if messages.count() > 100:
        # Delete the oldest messages, keeping only the latest 100
        messages_to_delete = messages[100:]
        messages_to_delete.delete()

@receiver(post_migrate)
def create_lobby_chat_room(sender, **kwargs):
    if sender.name == 'chat':
        if not ChatRoom.objects.filter(name='Lobby').exists():
            ChatRoom.objects.create(name='Lobby', is_public=True, is_group_chat=True, cover_image='lobby.svg')

@receiver(post_save, sender=Friend)
def create_private_chat_room(sender, instance, created, **kwargs):
    if created:
        user1 = instance.user
        user2 = instance.friend
        
        # Create a private chat room for the two friends
        room_name = ChatRoom.get_private_chat_roomname(user1, user2)
        room, created = ChatRoom.objects.get_or_create(name=room_name, is_public=False, is_group_chat=False)
        if created:
            room.members.add(user1, user2)