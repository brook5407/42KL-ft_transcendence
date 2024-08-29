from django.urls import path
from . import views

urlpatterns = [
	path('pong/pvp/', views.pong_pvp, name='pong.pvp'),
	path('pong/pve/', views.pong_pve, name='pong.pve'),
	path('pong/tournament/', views.pong_pvp, name='pong.tournament'),
]
