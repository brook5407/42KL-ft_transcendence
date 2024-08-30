from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRelationViewSet, FriendRequestViewSet, friend_list_drawer, friend_requests_drawer, search_friend_drawer, friend_profile_drawer, friend_chat_drawer

router = DefaultRouter()
router.register(r'friends', UserRelationViewSet, basename='friends')
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('api/', include(router.urls)),
    
    # drawers
    path('drawer/friend-list', friend_list_drawer, name='friend.list-drawer'),
    path('drawer/friend-requests', friend_requests_drawer, name='friend.requests-drawer'),
    path('drawer/search-friend', search_friend_drawer, name='friend.search-friend-drawer'),
    path('drawer/friend-drawer', friend_profile_drawer, name='friend.profile-drawer'),
    path('drawer/friend-room', friend_chat_drawer, name='friend.friend-room-drawer'),
]

