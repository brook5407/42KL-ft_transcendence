from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from dj_rest_auth.registration.views import RegisterView


urlpatterns = [
    path('signup', RegisterView.as_view(), name='signup'),
    path('signin', LoginView.as_view(), name='signin'),
    path('signout', LogoutView.as_view(), name='signout'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]