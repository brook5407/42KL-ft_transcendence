from django.contrib import admin
from .models import UserRelation, FriendRequest
# Register your models here.

admin.site.register(UserRelation)
admin.site.register(FriendRequest)
