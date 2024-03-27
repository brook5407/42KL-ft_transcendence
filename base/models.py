from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default='avatar.svg')

    def __str__(self):
        return f'{self.user.username} Profile'

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')
    block = models.ManyToManyField(User, related_name='block')

    def __str__(self):
        return f'{self.user.username} Friends'
