from django.urls import path
from .views import FriendManagementView, AcceptRequestView


urlpatterns = [
    path('friend', FriendManagementView.as_view(), name='friend_management'),
    path('accept-request', AcceptRequestView.as_view(), name='accept_request'),
]

