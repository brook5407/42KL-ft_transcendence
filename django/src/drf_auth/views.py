from allauth.account.adapter import DefaultAccountAdapter
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest, JsonResponse
import requests
from django.contrib import messages
from django.conf import settings

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

