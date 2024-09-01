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
from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer
from rest_framework.decorators import api_view


User = get_user_model()

class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_num = request.GET.get('group_num')
        return Response({'group_num': group_num})

class FriendChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_num = request.GET.get('group_num')
        return Response({'group_num': group_num})

class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, receiver_id):
        receiver = get_object_or_404(User, id=receiver_id)
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            chat_message = serializer.save(sender=request.user, receiver=receiver)
            return Response(ChatMessageSerializer(chat_message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, receiver_id):
        receiver = get_object_or_404(User, id=receiver_id)
        messages = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) | 
            (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/chat-list.html', {
        'public_chats': ChatRoom.objects.filter(is_public=True),
        'private_chats': ChatRoom.get_private_chats(request.user)
	})
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_room_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

    room_id = request.GET.get('room_id')
    if not room_id:
        return HttpResponseBadRequest("Error: Room ID is required.")
    
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
    
    return render(request, 'components/drawers/chat-room.html', {
        'room': room,
        'room_name': room.get_room_name(request.user),
        'messages': ChatMessageSerializer(messages, many=True).data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_friendroom_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

    room_id = request.GET.get('room_id')
    if not room_id:
        return HttpResponseBadRequest("Error: Room ID is required.")
    
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
    
    return render(request, 'components/drawers/chat-friendroom.html', {
        'room': room,
        'room_name': room.get_room_name(request.user),
        'messages': ChatMessageSerializer(messages, many=True).data
    })