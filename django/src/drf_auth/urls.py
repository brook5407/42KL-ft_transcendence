from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import LogoutView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from .views import EmailVerificationView, LoginViewCustom, SendOTPView

urlpatterns = [
    path('signup', RegisterView.as_view(), name='account_signup'),
    path('signin', LoginViewCustom.as_view(), name='account_login'),
    path('signout', LogoutView.as_view(), name='account_logout'),
    path("signup/verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path("signup/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("account-confirm-email/<str:key>/", VerifyEmailView.as_view(), name="account_confirm_email"),
    path("account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    path('verify/<str:key>/', EmailVerificationView.as_view(), name='verify_email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-otp', SendOTPView.as_view(), name='send_otp'),
]
