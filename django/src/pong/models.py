# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class GameRoom(models.Model):
    room_name = models.CharField(max_length=8, unique=True)
    is_full = models.BooleanField(default=False)

