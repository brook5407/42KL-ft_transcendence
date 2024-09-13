from rest_framework import serializers
from .models import ChatMessage, ChatRoom
from base.serializers import UserSerializer
from profiles.serializers import ProfileSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_public', 'cover_image']  # Adjust fields as needed

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    room = ChatRoomSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'room', 'created_at']
        
    def get_sender(self, obj):
        profile = obj.sender.profile
        return ProfileSerializer(profile).data
