from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('home', views.home, name='home'),

	path('current-user', views.current_user_profile, name='base.current-user'),

	# modals
	path('modal/signin-modal', views.signin_modal, name='base.signin-modal'),
	path('modal/signup-modal', views.signup_modal, name='base.signup-modal'),
	path('modal/oauth42-modal', views.oauth42_modal, name='base.oauth42-modal'),

	# drawers
	path('drawer/settings', views.settings_drawer, name='base.settings-drawer'),
]