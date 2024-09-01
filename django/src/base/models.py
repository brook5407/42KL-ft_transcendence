import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from .fields import RandomStringIDField


class BaseModel(models.Model):
    id = RandomStringIDField(primary_key=True, editable=False)

    class Meta:
        abstract = True
        

class CustomUser(AbstractUser):
    id = RandomStringIDField(primary_key=True, editable=False)

    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return self.username
