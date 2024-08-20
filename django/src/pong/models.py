from django.db import models
from django.contrib.auth.models import User
import uuid

# class GameRoom(models.Model):
#     room_name = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
#     player1 = models.ForeignKey(User, related_name='player1', on_delete=models.CASCADE)
#     player2 = models.ForeignKey(User, related_name='player2', null=True, blank=True, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
