from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("update_profile/", views.profileUpdateView, name="update_profile"),
    path("settings/", views.settings, name="settings"),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),
]