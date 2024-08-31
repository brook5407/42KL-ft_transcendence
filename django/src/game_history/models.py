from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GameHistory(models.Model):
    player1 = models.ForeignKey(User, related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='games_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='games_won', on_delete=models.CASCADE)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()
    mode = models.CharField(max_length=20)
    game_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player1} vs {self.player2}"
