from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("accounts/update_profile/", views.profileUpdateView, name="update_profile"),
    path('accounts/profile/', views.profile, name='profile')
]