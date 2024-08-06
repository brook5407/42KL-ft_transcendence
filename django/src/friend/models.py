from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_relations")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_relations", default=None)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
    
    