from django.urls import path
from .views import FriendManagementView, FriendRequestView


urlpatterns = [
    path('friend', FriendManagementView.as_view(), name='friend_management'),
    path('friend_request', FriendRequestView.as_view(), name='friend_request'),
]

