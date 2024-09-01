# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatMessage


User = get_user_model()

class ChatMessageSerializer(serializers.ModelSerializer):
    # sender = UserSerializer(read_only=True)
    # room = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'room', 'timestamp']