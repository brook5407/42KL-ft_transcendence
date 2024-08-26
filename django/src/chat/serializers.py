# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    # sender = UserSerializer(read_only=True)
    # room = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'room', 'timestamp']