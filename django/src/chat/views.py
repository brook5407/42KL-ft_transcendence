# views.py
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from utils.request_helpers import is_ajax_request
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/chat-list.html', {
        'public_chats': ChatRoom.objects.filter(is_public=True),
        'private_chats': ChatRoom.get_private_chats(request.user) # WXR TODO: frontend dynamic fetch user's active private chats
	})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
