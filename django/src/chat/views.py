# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer, UserSerializer

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