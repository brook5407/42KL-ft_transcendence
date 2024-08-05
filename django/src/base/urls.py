from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('home', views.home, name='home'),

	# modals
	path('modal/signin-modal', views.signin_modal, name='signin-modal'),
	path('modal/signup-modal', views.signup_modal, name='signup-modal'),
	path('modal/oauth42-modal', views.oauth42_modal, name='oauth42-modal'),

	# drawers
	path('drawer/profile', views.profile_drawer, name='profile-drawer'),
	path('drawer/settings', views.settings_drawer, name='settings-drawer'),

	# catch all
    re_path(r'^(?!accounts/|admin/|static/|media/).*$', views.index, name='catchall'),
]