from allauth.account.adapter import DefaultAccountAdapter
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
import requests
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model

# import username 
# from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .utils import send_otp_email
from .models import OnetimePassword
from dj_rest_auth.views import LoginView
from dj_rest_auth.app_settings import api_settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        app_url = settings.APP_URL
        confirmation_key = emailconfirmation.key
        return f'{app_url}/auth/verify/{confirmation_key}/'
    

class EmailVerificationView(View):
    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not key:
            messages.error(request, 'Verification key is missing')
            return redirect(settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL)
        
        # You can render your index.html template here if needed
        # For now, we'll just proceed with the POST request
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not key:
            messages.error(request, 'Verification key is missing')
            return redirect(settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL)

        # Construct the URL for the VerifyEmailView
        verify_url = request.build_absolute_uri(reverse('account_confirm_email', kwargs={'key': key}))

        # Prepare the data to be sent in the request body
        data = {'key': key}

        # Make a POST request to the VerifyEmailView with the key in the body
        try:
            response = requests.post(verify_url, json=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses
        except requests.RequestException as e:
            messages.error(request, {"error": str(e)})
            return redirect(settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL)

        if response.status_code == 200:
            # Successful verification
            messages.success(request, 'Your email has been successfully verified.')
            return redirect(settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL)
        else:
            messages.error(request, 'There was an error verifying your email.')
            return redirect(settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL)
            # Handle error cases


class SendOTPView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = api_settings.LOGIN_SERIALIZER

    def post(self, request):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        if self.serializer.is_valid(raise_exception=True):
            data = self.serializer.data
            try:
                user = get_user_model().objects.get(username=data['username'])
                email_address = EmailAddress.objects.get(user=user)
                if email_address.verified:
                    send_otp_email(user.email)
                    return Response({
                        'non_field_errors': ['OTP sent. Please check your email.'],
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'non_field_errors': ['User email is not verified.']
                    }, status=status.HTTP_400_BAD_REQUEST)
            except user.DoesNotExist:
                return Response({
                    'non_field_errors': ['User does not exist.']
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewCustom(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['OTP_AUTH'] = settings.OTP_AUTH  # Add the OTP_AUTH setting to the context
        return context

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        if settings.OTP_AUTH:
            data = self.request.data
            user = get_user_model().objects.get(username=data['username'])
            otp = OnetimePassword.objects.get(user=user)
            otp_input = data['otp'].strip()
            if otp.code != otp_input:
                return Response({
                    'non_field_errors': ['OTP is invalid']
                }, status=status.HTTP_400_BAD_REQUEST)
            elif otp.code == otp_input:
                if otp.check_expired():
                    return Response({
                        'non_field_errors': ['OTP has expired, Please request a new one']
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'non_field_errors': ['OTP is invalid']
                }, status=status.HTTP_400_BAD_REQUEST)

            otp.delete()

        self.login()
        return self.get_response()
