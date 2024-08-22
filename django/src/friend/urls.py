from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRelationViewSet, FriendRequestViewSet

router = DefaultRouter()
router.register(r'user-relations', UserRelationViewSet)
router.register(r'friend-requests', FriendRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

