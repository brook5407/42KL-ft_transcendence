from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        app_url = settings.APP_URL
        confirmation_key = emailconfirmation.key
        return f'{app_url}/verify/{confirmation_key}/'
    
