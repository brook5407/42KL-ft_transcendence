from django.urls import re_path
from .consumers import FriendRequestConsumer, OnlineStatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/friend-requests/$', FriendRequestConsumer.as_asgi()),
    re_path(r'ws/online-status/$', OnlineStatusConsumer.as_asgi()),
]