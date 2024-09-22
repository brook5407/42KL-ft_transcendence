from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from base.models import BaseModel


User = get_user_model()

# Create your models here.
class OnetimePassword(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expired_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(minutes=1)
        super(OnetimePassword, self).save(*args, **kwargs)

    def check_expired(self):
        return self.expired_at < timezone.now()

