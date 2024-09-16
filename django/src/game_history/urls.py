from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameHistoryViewSet, game_history_drawer

router = DefaultRouter()
router.register(r'gamehistory', GameHistoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    # drawers
    path('drawer/game-history-drawer/', game_history_drawer, name='game-history.drawer'),
]