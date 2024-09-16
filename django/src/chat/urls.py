# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatMessageViewSet, ActiveChatRoomViewSet, chat_list_drawer, chat_room_drawer

router = DefaultRouter()
router.register(r'chat-message', ChatMessageViewSet, basename='chat-message')
router.register(r'active-chat', ActiveChatRoomViewSet, basename='active-chat')

urlpatterns = [
	# drawers
	path('drawer/chat-list', chat_list_drawer, name='chat.list-drawer'),
	path('drawer/chat-room', chat_room_drawer, name='chat.room-drawer'),
	
    path('api/', include(router.urls)),
]