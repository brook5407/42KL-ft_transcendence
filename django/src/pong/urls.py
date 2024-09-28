from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"tournament-room", views.TournamentRoomViewSet)
router.register(r"match-history", views.MatchHistoryViewSet)

urlpatterns = [
    path("pong/pvp/", views.pvp_view, name="pong.pvp"),
    path("pong/pve/", views.pve_view, name="pong.pve"),
    path("pong/local/", views.local_view, name="pong.local"),
    path("pong/tournament/", views.tournament_view, name="pong.tournament"),
    path("api/", include(router.urls)),
    # drawers
    path("drawer/tournament-list/", views.tournament_list_drawer, name="pong.tournament-list-drawer"),
    path("drawer/tournament-create/", views.tournament_create_drawer, name="pong.tournament-create-drawer"),
    path("drawer/tournament-room/", views.tournament_room_drawer, name="pong.tournament-room-drawer"),
    path('drawer/match-history-drawer/', views.match_history_drawer, name='pong.match-history-drawer'),
]
