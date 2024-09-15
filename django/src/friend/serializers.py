from rest_framework import serializers

from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from .models import UserRelation, FriendRequest
from base.serializers import UserSerializer

class UserRelationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    friend = serializers.SerializerMethodField()

    class Meta:
        model = UserRelation
        fields = ['id', 'user', 'friend', 'blocked', 'blocked_at', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        profile = Profile.objects.get(user=obj.user)
        return ProfileSerializer(profile).data

    def get_friend(self, obj):
        profile = Profile.objects.get(user=obj.friend)
        return ProfileSerializer(profile).data
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['friend'] = self.get_friend(instance)
        return ret

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']
    
    def get_sender(self, obj):
        profile = Profile.objects.get(user=obj.sender)
        return ProfileSerializer(profile).data

    def get_receiver(self, obj):
        profile = Profile.objects.get(user=obj.receiver)
        return ProfileSerializer(profile).data
