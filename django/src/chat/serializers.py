from rest_framework import serializers
from .models import ChatMessage, ChatRoom, ActiveChatRoom
from base.serializers import UserSerializer
from profiles.serializers import ProfileSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_public', 'cover_image', 'is_group_chat']
    
    def to_representation(self, instance):
        # for private chat room, return the other user's nickname as the room name
        representation = super().to_representation(instance)
        if not instance.is_public and instance.members.count() == 2:
            request = self.context.get('request')
            if request:
                current_user = request.user
                other_user = instance.members.exclude(id=current_user.id).first()
                if other_user:
                    representation['name'] = other_user.profile.nickname
        return representation

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    room = ChatRoomSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'room', 'created_at']
        
    def get_sender(self, obj):
        profile = obj.sender.profile
        return ProfileSerializer(profile).data
    

class ActiveChatRoomSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = ChatRoomSerializer(read_only=True)
    last_message = ChatMessageSerializer(read_only=True)

    class Meta:
        model = ActiveChatRoom
        fields = ['id', 'user', 'room', 'last_message', 'unread_count']
