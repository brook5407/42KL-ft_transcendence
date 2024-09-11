from django.urls import re_path, path
from chat import consumers

websocket_urlpatterns = [
	re_path(r'room/(?P<group_num>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/drawer/chat-friendroom/(?P<group_num>\w+)/$', consumers.ChatConsumer.as_asgi()),
]