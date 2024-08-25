from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView

urlpatterns = [
    path('signup', RegisterView.as_view(), name='signup'),
    path('signin', LoginView.as_view(), name='signin'),
    path('signout', LogoutView.as_view(), name='signout'),
]
