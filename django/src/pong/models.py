# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class GameRoom(models.Model):
    room_name = models.CharField(max_length=8, unique=True)
    is_full = models.BooleanField(default=False)

class Player(models.Model):
    username = models.CharField(max_length=100)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    elo = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Match(models.Model):
    player1 = models.ForeignKey(User, related_name='matches_as_player1', on_delete=models.SET_NULL, null=True, blank=True)
    player2 = models.ForeignKey(User, related_name='matches_as_player2', on_delete=models.SET_NULL, null=True, blank=True)
    winner = models.ForeignKey(User, related_name='matches_won', on_delete=models.SET_NULL, null=True, blank=True)
    room_name = models.CharField(max_length=5, unique=True)
    is_full = models.BooleanField(default=False)

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    current_round = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MatchHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_matches')
    opponent = models.OneToOneField(User, on_delete=models.CASCADE, related_name='opponent_matches')
    won = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} vs {self.opponent.username} - {'Won' if self.won else 'Lost'}"
