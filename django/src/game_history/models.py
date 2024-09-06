from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from enum import Enum


User = get_user_model()

class WinsLosses(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)


class GameHistory(BaseModel):
    class GameMode(Enum):
        PVP = 'pvp'
        PVE = 'pve'

    player1 = models.ForeignKey(User, related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='games_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='games_won', on_delete=models.CASCADE)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()
    mode = models.CharField(
        max_length=20,
        choices=[(tag, tag.value) for tag in GameMode],
        default=GameMode.PVP
    )

    def __str__(self):
        return f"{self.player1} vs {self.player2}"
