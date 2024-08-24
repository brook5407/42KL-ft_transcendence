from rest_framework import serializers
from .models import Profile
from base.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'bio', 'avatar']