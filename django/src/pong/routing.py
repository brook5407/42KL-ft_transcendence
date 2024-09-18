from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/matchmaking/$', consumers.MatchMakingConsumer.as_asgi()),
    re_path(r'ws/(?P<game_mode>\w+)/(?P<room_id>\w+)/$', consumers.PongConsumer.as_asgi()),
    re_path(r'ws/tournament/$', consumers.TournamentConsumer.as_asgi()),
]
