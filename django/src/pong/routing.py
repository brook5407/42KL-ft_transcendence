from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<game_mode>\w+)/(?P<room_name>\w+)/$', consumers.PVPConsumer.as_asgi()),
]
