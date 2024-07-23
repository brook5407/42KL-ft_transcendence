from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup', UserRegistrationAPIView.as_view(), name='signup'),
    path('signin', UserLoginAPIView.as_view(), name='signin'),
	path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]