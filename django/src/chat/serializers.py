from rest_framework import serializers
from .models import ChatMessage, ChatRoom, ActiveChatRoom
from base.serializers import UserSerializer
from pong.serializers import MatchInvitationSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_public', 'cover_image', 'is_group_chat']
        
    def to_representation(self, instance):
        # for private chat room, return the other user's nickname as the room name
        # and the cover image as the other user's profile picture
        representation = super().to_representation(instance)
        if not instance.is_public and instance.members.count() == 2:
            request = self.context.get('request')
            if request:
                current_user = request.user
                other_user = instance.members.exclude(id=current_user.id).first()
                if other_user:
                    profile = other_user.profile
                    representation['name'] = profile.nickname
                    representation['cover_image'] = profile.avatar.url
        return representation

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    room = ChatRoomSerializer(read_only=True)
    match_invitation = MatchInvitationSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'room', 'match_invitation', 'created_at']
    

class ActiveChatRoomSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = ChatRoomSerializer(read_only=True)
    last_message = ChatMessageSerializer(read_only=True)

    class Meta:
        model = ActiveChatRoom
        fields = ['id', 'user', 'room', 'last_message', 'unread_count']
