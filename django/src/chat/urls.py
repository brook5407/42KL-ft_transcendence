# urls.py
from django.urls import path
from .views import ChatAPIView, FriendChatAPIView, SendMessageAPIView, ChatHistoryAPIView

urlpatterns = [
    path('', ChatAPIView.as_view(), name='chat'),
    path('friendchat', FriendChatAPIView.as_view(), name='friendchat'),
    path('send_message/<int:receiver_id>', SendMessageAPIView.as_view(), name='send_message'),
    path('chat_history/<int:receiver_id>', ChatHistoryAPIView.as_view(), name='chat_history'),
]