# urls.py
from django.urls import path
from .views import ChatAPIView, FriendChatAPIView, SendMessageAPIView, ChatHistoryAPIView, chat_list_drawer, chat_room_drawer, chat_friendroom_drawer

urlpatterns = [
	# drawers
	path('drawer/chat-list', chat_list_drawer, name='chat.list-drawer'),
	path('drawer/chat-room', chat_room_drawer, name='chat.room-drawer'),
	path('drawer/chat-friendroom', chat_friendroom_drawer, name='chat.friendroom-drawer'),
	
    path('chat', ChatAPIView.as_view(), name='chat'),
    path('friendchat', FriendChatAPIView.as_view(), name='chat.friendchat'),
    path('send_message/<int:receiver_id>', SendMessageAPIView.as_view(), name='chat.send_message'),
    path('chat_history/<int:receiver_id>', ChatHistoryAPIView.as_view(), name='chat.chat_history'),
]