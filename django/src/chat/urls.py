# urls.py
from django.urls import path
# from .views import ChatAPIView, FriendChatAPIView, SendMessageAPIView, ChatHistoryAPIView, chat_list_drawer, chat_room_drawer
from .views import ChatAPIView, FriendChatAPIView, SendMessageAPIView, ChatHistoryAPIView, chat_list_drawer, chat_room_drawer, chat_friendroom_drawer, get_paginated_messages, fetch_chat_messages

urlpatterns = [
	# drawers
	path('drawer/chat-list', chat_list_drawer, name='chat.list-drawer'),
	path('drawer/chat-room', chat_room_drawer, name='chat.room-drawer'),
	path('drawer/chat-friendroom', chat_friendroom_drawer, name='chat.friendroom-drawer'),
	
    # path('chatroom/<uuid:room_id>/messages/', fetch_chat_messages, name='chat.fetch_chat_messages'),
    path('chatroom/<int:room_id>/messages/', get_paginated_messages, name='chat.get_paginated_messages'),
    path('chat', ChatAPIView.as_view(), name='chat'),
    path('friendchat', FriendChatAPIView.as_view(), name='chat.friendchat'),
    path('send_message/<int:receiver_id>', SendMessageAPIView.as_view(), name='chat.send_message'),
    path('chat_history/<int:receiver_id>', ChatHistoryAPIView.as_view(), name='chat.chat_history'),
]