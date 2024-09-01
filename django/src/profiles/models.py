from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel


User = get_user_model()

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, upload_to='avatars/', default='avatar.svg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.user.username
        super().save(*args, **kwargs)

    def get_avatar_url(self):
        if not self.avatar:
            return 'https://www.gravatar.com/avatar/'
        return self.avatar.url