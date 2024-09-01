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
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes


User = get_user_model()

class UserRelationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRelationSerializer
    
    def get_queryset(self):
        return UserRelation.objects.filter(user=self.request.user, deleted=False)

    @action(detail=False, methods=['post'])
    def block(self, request):
        friend_id = request.data.get('friend_id')
        if not friend_id:
            return Response({'error': 'friend_id is required'}, status=400)
        user_relation = get_object_or_404(UserRelation, user=request.user, friend=friend_id)
        user_relation.block()
        return Response({'status': 'friend blocked'})

    @action(detail=False, methods=['post'])
    def unblock(self, request):
        friend_id = request.data.get('friend_id')
        if not friend_id:
            return Response({'error': 'friend_id is required'}, status=400)
        user_relation = get_object_or_404(UserRelation, user=request.user, friend=friend_id)
        user_relation.unblock()
        return Response({'status': 'friend unblocked'})

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        friend_id = request.query_params.get('friend_id')
        if not friend_id:
            return Response({'error': 'friend_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_relation = get_object_or_404(UserRelation, user=request.user, friend=friend_id)
        user_relation.delete()
        return Response({'status': 'friend deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def search_friend(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'status': 'username query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        if user == request.user:
            return Response({'status': 'cannot add yourself as a friend'}, status=status.HTTP_400_BAD_REQUEST)
        elif UserRelation.objects.filter(user=request.user, friend=user, deleted=False).exists():
            return Response({'status': 'already friends'}, status=status.HTTP_400_BAD_REQUEST)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        response_data = serializer.data
        is_friend = user.friends.filter(id=request.user.id).exists()
        latest_friend_request = FriendRequest.objects.filter(sender=request.user, receiver=user).order_by('-created_at').first()
        can_add_friend = (not is_friend) and (latest_friend_request is None or latest_friend_request.status != FriendRequest.Status.PENDING)
        response_data['is_friend'] = is_friend
        response_data['can_add_friend'] = can_add_friend
        return Response(response_data, status=status.HTTP_200_OK)


class FriendRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        if friend_request.receiver != request.user:
            return Response({'status': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)
        friend_request.accept(request.user)
        return Response({'status': 'friend request accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        if friend_request.receiver != request.user:
            return Response({'status': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)
        friend_request.reject(request.user)
        return Response({'status': 'friend request rejected'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_username = request.data.get('receiver')
        receiver = get_object_or_404(User, username=receiver_username)
        
        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status=FriendRequest.Status.PENDING).exists():
            return Response({'status': 'friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(
            sender=sender,
            receiver=receiver,
        )
        
        return Response({'status': 'friend request sent'}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def to_me(self, request):
        friend_requests = FriendRequest.objects.filter(receiver=request.user).order_by('-created_at')
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_list_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/friend/list.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/friend/requests.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_friend_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/friend/search-friend.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_profile_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    friend_user = User.objects.get(username=request.GET.get('username'))
    is_blocked = UserRelation.objects.filter(user=request.user, friend=friend_user, blocked=True).exists()
    return render(request, 'components/drawers/friend/profile.html', {
        'friend_profile': Profile.objects.get(user=friend_user),
        'friend_is_blocked': is_blocked
    })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_chat_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    friend_user = User.objects.get(username=request.GET.get('username'))
    return render(request, 'components/drawers/chat-friendroom.html', {
        'friend_profile': Profile.objects.get(user=friend_user)
    })
