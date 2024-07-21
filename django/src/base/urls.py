from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('home', views.home, name='home'),
	path('signin', views.signin, name='signin'),
    re_path(r'^.*$', views.index, name='catchall'),
]