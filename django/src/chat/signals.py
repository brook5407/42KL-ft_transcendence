# signals.py
from django.db.models.signals import post_save, post_migrate, m2m_changed
from django.dispatch import receiver
from .models import ChatMessage, ChatRoom, ActiveChatRoom
from friend.models import UserRelation as Friend
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(post_save, sender=ChatMessage)
def limit_public_chat_messages(sender, instance, **kwargs):
    room = instance.room
    if room is None:
        return
    if not room.is_public:
        return
    messages = ChatMessage.objects.filter(room=room).order_by('-created_at')
    if messages.count() > 100:
        # Delete the oldest messages, keeping only the latest 100
        messages_to_delete = messages[100:]
        messages_to_delete.delete()

@receiver(post_migrate)
def create_lobby_chat_room(sender, **kwargs):
    # Create a lobby chat room if it doesn't exist after migration
    if sender.name == 'chat':
        if not ChatRoom.objects.filter(name='Lobby').exists():
            ChatRoom.objects.create(name='Lobby', is_public=True, is_group_chat=True, cover_image='lobby.svg')

@receiver(post_save, sender=User)
def create_lobby_chat_room_for_new_user(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.is_superuser:
        return
    lobby_room, created = ChatRoom.objects.get_or_create(name='Lobby', is_public=True, is_group_chat=True, cover_image='lobby.svg')
    lobby_last_message = lobby_room.get_last_message()
    ActiveChatRoom.objects.get_or_create(user=instance, room=lobby_room, last_message=lobby_last_message)

@receiver(post_save, sender=Friend)
def create_private_chat_room(sender, instance, created, **kwargs):
    if not created:
        return
    user1 = instance.user
    user2 = instance.friend
    # Create a private chat room for the two friends
    room_name = ChatRoom.get_private_chat_roomname(user1, user2)
    room, chatroom_created = ChatRoom.objects.get_or_create(name=room_name, is_public=False, is_group_chat=False)
    if chatroom_created:
        room.members.add(user1, user2)
        
@receiver(m2m_changed, sender=ChatRoom.members.through)
def create_active_chat_room(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        new_members = User.objects.filter(pk__in=pk_set)
        for member in new_members:
            active_chatroom, created = ActiveChatRoom.objects.get_or_create(user=member, room=instance)
                
@receiver(post_save, sender=ChatMessage)
def update_active_chat_room(sender, instance, **kwargs):
    room = instance.room
    if room is None:
        return
    active_chatrooms = ActiveChatRoom.objects.filter(room=room)
    for active_chatroom in active_chatrooms:
        active_chatroom.last_message = instance
        if active_chatroom.user != instance.sender:
            active_chatroom.unread_count += 1
        active_chatroom.save()
        