from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserRelation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserRelationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserRelation
        fields = ['id', 'user', 'friend', 'accepted']

