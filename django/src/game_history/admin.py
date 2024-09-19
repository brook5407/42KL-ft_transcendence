from django.contrib import admin

# Register your models here.
from .models import GameHistory, WinsLosses

admin.site.register(GameHistory)
admin.site.register(WinsLosses)
