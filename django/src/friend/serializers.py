from rest_framework import serializers

from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from .models import UserRelation, FriendRequest
from base.serializers import UserSerializer

class UserRelationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)

    class Meta:
        model = UserRelation
        fields = ['id', 'user', 'friend', 'deleted', 'deleted_at', 'blocked', 'blocked_at', 'created_at', 'updated_at']

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'sender_words', 'reject_reason', 'created_at', 'updated_at']
    
    def get_sender(self, obj):
        profile = Profile.objects.get(user=obj.sender)
        return ProfileSerializer(profile).data

    def get_receiver(self, obj):
        profile = Profile.objects.get(user=obj.receiver)
        return ProfileSerializer(profile).data
