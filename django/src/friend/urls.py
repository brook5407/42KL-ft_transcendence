from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRelationViewSet, FriendRequestViewSet, friend_list_drawer, friend_requests_drawer

router = DefaultRouter()
router.register(r'user-relations', UserRelationViewSet)
router.register(r'friend-requests', FriendRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # drawers
    path('drawer/friend-list', friend_list_drawer, name='friend.list-drawer'),
    path('drawer/friend-requests', friend_requests_drawer, name='friend.requests-drawer'),
]

