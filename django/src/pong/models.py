# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class GameRoom(models.Model):
    room_name = models.CharField(max_length=8, unique=True)
    is_full = models.BooleanField(default=False)

class MatchHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_matches')
    opponent = models.OneToOneField(User, on_delete=models.CASCADE, related_name='opponent_matches')
    won = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} vs {self.opponent.username} - {'Won' if self.won else 'Lost'}"
