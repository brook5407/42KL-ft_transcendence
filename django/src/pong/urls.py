from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"tournament-room", views.TournamentRoomViewSet)
router.register(r"matchmaking", views.MatchViewSet)

urlpatterns = [
    path("pong/pvp/", views.pvp_view, name="pong.pvp"),
    path("pong/pve/", views.pve_view, name="pong.pve"),
    path("api/", include(router.urls)),
    # drawers
    path("drawer/tournament-list/", views.tournament_list_drawer, name="pong.tournament-list-drawer"),
    path("drawer/tournament-create/", views.tournament_create_drawer, name="pong.tournament-create-drawer"),
]
