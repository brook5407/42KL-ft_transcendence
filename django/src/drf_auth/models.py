from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class OnetimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(minutes=2)
        super(OnetimePassword, self).save(*args, **kwargs)

    def check_expired(self):
        return self.expired_at < timezone.now()

