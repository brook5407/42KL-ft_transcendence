from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameHistoryViewSet

router = DefaultRouter()
router.register(r'game-history', GameHistoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]