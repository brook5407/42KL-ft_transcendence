from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
    
    def get_profile(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
            return ProfileSerializer(profile).data
        except Profile.DoesNotExist:
            return None