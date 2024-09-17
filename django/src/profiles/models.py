from django.db import models
from django.contrib.auth import get_user_model
from django.templatetags.static import static
from base.models import BaseModel
from game_history.models import WinsLosses


User = get_user_model()

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, upload_to='avatars/', default='avatar.svg')
    language = models.CharField(max_length=7, default='en')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.user.username
        super().save(*args, **kwargs)

    def get_avatar_url(self):
        if not self.avatar:
            return static('images/avatar.svg')
        return self.avatar.url
    
    def get_wins_losses(self):
        model, created = WinsLosses.objects.get_or_create(user=self.user)
        return model.wins, model.losses
