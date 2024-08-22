from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import UserRelation, FriendRequest
from .serializers import UserRelationSerializer, FriendRequestSerializer
from django.contrib.auth.models import User

class UserRelationViewSet(viewsets.ModelViewSet):
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
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        friend_request.accept(request.user)
        return Response({'status': 'friend request accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        friend_request.reject(request.user)
        return Response({'status': 'friend request rejected'})

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_username = request.data.get('receiver')
        receiver = get_object_or_404(User, username=receiver_username)
        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({'status': 'friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response({'status': 'friend request sent'}, status=status.HTTP_201_CREATED)