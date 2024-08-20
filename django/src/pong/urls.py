from django.urls import path
from . import views

urlpatterns = [
	path('pong/index/', views.pong, name='pong.index'),
]
