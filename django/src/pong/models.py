# models.py
from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
import uuid


User = get_user_model()

class GameRoom(BaseModel):
    room_name = models.CharField(max_length=8, unique=True)
    is_full = models.BooleanField(default=False)
    players = models.ManyToManyField('Player')

class Tournament(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),        # Tournament is in the lobby, waiting for players
        ('ongoing', 'Ongoing'),        # Tournament has started
        ('completed', 'Completed'),    # Tournament is finished
    ]
    room = models.OneToOneField(GameRoom, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return self.room

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, blank=True)
    # tournaments = models.ManyToManyField(Tournament, related_name='players')
    # wins = models.IntegerField(default=0)
    # losses = models.IntegerField(default=0)
    # elo = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True)
    room_name = models.CharField(max_length=5, unique=True)
    is_full = models.BooleanField(default=False)
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_player1', null=True, blank=True)
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_player2', null=True, blank=True)
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='match_winner')

    def __str__(self):
        return f"{self.tournament.name if self.tournament else 'PVP Match'} - {self.player1} vs {self.player2}"