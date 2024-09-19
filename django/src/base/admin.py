from django.contrib import admin
from .models import CustomUser, BaseModel
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(BaseModel)
