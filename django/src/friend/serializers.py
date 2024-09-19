from rest_framework import serializers
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from .models import UserRelation, FriendRequest
from base.serializers import UserSerializer

class UserRelationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friend = UserSerializer()

    class Meta:
        model = UserRelation
        fields = ['id', 'user', 'friend', 'blocked', 'blocked_at', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['friend'] = UserSerializer(instance.friend).data
        return ret

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']
