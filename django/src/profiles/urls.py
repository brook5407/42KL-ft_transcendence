from django.urls import path, re_path
from . import views

urlpatterns = [
	# drawers
	path('drawer/profile/', views.profile_drawer, name='profile.drawer'),

	# api
	path('profile/detail/', views.ProfileDetail.as_view(), name='profile.detail'),
]