from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("update_profile/", views.profileUpdateView, name="update_profile"),
    path("settings/", views.settings, name="settings"),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),
    path('pong/', views.pong, name='pong'),
	path('game/<str:room_name>/', views.game, name='game'),
    path('create_room/', views.create_room, name='create_room'),
    path('lobby/', views.lobby, name='lobby'),
]