from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings


# Create your models here.
from django.db import models
from .fields import RandomStringIDField

class BaseModel(models.Model):
    id = RandomStringIDField(primary_key=True)

    class Meta:
        abstract = True
