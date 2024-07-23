from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('home', views.home, name='home'),
	path('signin-modal', views.signin_modal, name='signin-modal'),
	path('signup-modal', views.signup_modal, name='signup-modal'),
	path('oauth42-modal', views.oauth42_modal, name='oauth42-modal'),
    re_path(r'^(?!accounts/).*$', views.index, name='catchall'),
]