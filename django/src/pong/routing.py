from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<game_mode>\w+)/(?P<room_name>\w+)/$', consumers.PongConsumer.as_asgi()),
    # re_path(r'ws/tournament/(?P<room_name>\w+)/$', consumers.TournamentConsumer.as_asgi()),
]
