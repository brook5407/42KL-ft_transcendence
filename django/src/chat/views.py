# views.py
from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from utils.request_helpers import is_ajax_request, authenticated_view
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Q
from .models import ChatMessage, ChatRoom, ActiveChatRoom
from .serializers import ChatMessageSerializer, ActiveChatRoomSerializer
from .pagination import ChatMessagePagination, ActiveChatRoomsPagination


User = get_user_model()

class ChatMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = ChatMessagePagination
    serializer_class = ChatMessageSerializer

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        room = get_object_or_404(ChatRoom, id=pk)
        messages = ChatMessage.objects.filter(room=room).order_by('-created_at')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(messages, request, view=self)
        if page is not None:
            serializer = ChatMessageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


class ActiveChatRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = ActiveChatRoomsPagination
    serializer_class = ActiveChatRoomSerializer

    def get_queryset(self):
        return ActiveChatRoom.objects.filter(
                Q(last_message__isnull=False) | Q(room__is_public=True),
                user=self.request.user
            ).order_by('-last_message__created_at')

    def list(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = ActiveChatRoomSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        serializer = ActiveChatRoomSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='get-from-roomid/(?P<room_id>[^/.]+)')
    def get_from_roomid(self, request, room_id=None):
        user = request.user
        queryset = self.get_queryset().filter(room_id=room_id, user=user)
        active_chat = get_object_or_404(queryset)
        serializer = ActiveChatRoomSerializer(active_chat, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='mark-read/(?P<room_id>[^/.]+)')
    def mark_read(self, request, room_id=None):
        user = request.user
        active_chat = get_object_or_404(ActiveChatRoom, room_id=room_id, user=user)
        active_chat.unread_count = 0
        active_chat.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authenticated_view
def chat_list_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/chat-list.html')

@api_view(['GET'])
@authenticated_view
def chat_room_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

    room_id = request.GET.get('room_id')
    friend_username = request.GET.get('username')
    if room_id:
        room = get_object_or_404(ChatRoom, id=room_id)
    elif friend_username:
        friend = get_object_or_404(User, username=friend_username)
        room = get_object_or_404(ChatRoom, name=ChatRoom.get_private_chat_roomname(request.user, friend))
    else:
        return HttpResponseBadRequest("Error: Invalid request parameters.")
    return render(request, 'components/drawers/chat-room.html', {
                'room': room,
                'room_name': room.get_room_name(request.user),
            })
