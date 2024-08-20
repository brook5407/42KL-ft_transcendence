from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.
class OnetimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
