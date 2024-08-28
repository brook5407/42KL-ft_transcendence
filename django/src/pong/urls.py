from django.urls import path
from . import views

urlpatterns = [
	path('pong/pvp/', views.pong, name='pong.pvp'),
	path('pong/index/', views.pong, name='pong.index'),
	path('pong/index/', views.pong, name='pong.tournament'),
]
