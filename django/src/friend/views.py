from django.http import HttpResponseBadRequest
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render

from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from utils.request_helpers import is_ajax_request
from .models import UserRelation, FriendRequest
from .serializers import UserRelationSerializer, FriendRequestSerializer
from django.contrib.auth.models import User

class UserRelationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserRelation.objects.all()
    serializer_class = UserRelationSerializer

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        user_relation = get_object_or_404(UserRelation, pk=pk)
        user_relation.block()
        return Response({'status': 'friend blocked'})

    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        user_relation = get_object_or_404(UserRelation, pk=pk)
        user_relation.unblock()
        return Response({'status': 'friend unblocked'})

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        user_relation = get_object_or_404(UserRelation, pk=pk)
        user_relation.delete()
        return Response({'status': 'friend deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def search_friend(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        if user == request.user:
            return Response({'error': 'cannot add yourself as a friend'}, status=status.HTTP_400_BAD_REQUEST)
        elif UserRelation.objects.filter(user=request.user, friend=user).exists():
            return Response({'error': 'already friends'}, status=status.HTTP_400_BAD_REQUEST)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        friend_request.accept(request.user)
        return Response({'status': 'friend request accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        friend_request_id = request.data.get('friend_request_id')
        reject_reason = request.data.get('reject_reason', '')
        friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
        
        if friend_request.receiver != request.user:
            return Response({'status': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        friend_request.reject(request.user, reject_reason)
        
        return Response({'status': 'friend request rejected'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_username = request.data.get('receiver')
        sender_words = request.data.get('sender_words', f'Hi I am {sender.username}')
        receiver = get_object_or_404(User, username=receiver_username)
        
        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status=FriendRequest.Status.PENDING).exists():
            return Response({'status': 'friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(
            sender=sender,
            receiver=receiver,
            sender_words=sender_words
        )
        
        return Response({'status': 'friend request sent'}, status=status.HTTP_201_CREATED)
    
def friend_list_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/friend/list.html')

def friend_requests_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/friend/requests.html')

def search_friend_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/friend/search-friend.html')
