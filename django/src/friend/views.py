from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
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
    return render(request, 'components/drawers/friend/list.html')

def friend_requests_drawer(request):
    return render(request, 'components/drawers/friend/requests.html')