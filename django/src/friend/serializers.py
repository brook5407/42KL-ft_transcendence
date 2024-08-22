from rest_framework import serializers
from .models import UserRelation, FriendRequest
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRelationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)

    class Meta:
        model = UserRelation
        fields = ['id', 'user', 'friend', 'deleted', 'deleted_at', 'blocked', 'blocked_at', 'created_at', 'updated_at']

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'sender_words', 'reject_reason', 'created_at', 'updated_at']