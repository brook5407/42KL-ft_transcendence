from django.urls import path
from . import views

urlpatterns = [
	path('pong/pvp/', views.pvp_view, name='pong.pvp'),
	path('pong/pve/', views.pve_view, name='pong.pve'),
	path('pong/tournament/', views.tournament_view, name='pong.tournament'),
	path('pong/tournament/create', views.tournament_create_view, name='pong.tournament_create'),
	path('pong/tournament/<str:room_name>', views.tournament_join_view, name='pong.tournament_join'),
]
