import requests
from django.urls import reverse
from django.conf import settings
from allauth.account import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Error,
)
from allauth.utils import build_absolute_uri
from core import settings
from .client import FortyTwoOAuth2Client
from .provider import FortyTwoProvider
from rest_framework_simplejwt.tokens import RefreshToken


class FortyTwoOAuth2Adapter(OAuth2Adapter):
    provider_id = FortyTwoProvider.id
    redirect_uri_protocol = None
    access_token_method = "POST"
    access_token_url = f'{settings.FT_OAUTH_SERVER_BASE_URL}/oauth/token'
    profile_url = f'{settings.FT_OAUTH_SERVER_BASE_URL}/v2/me'
    authorize_url = f'{settings.FT_OAUTH_SERVER_BASE_URL}/oauth/authorize'

    def get_callback_url(self, request, app):
        callback_url = reverse(self.provider_id + "_callback")
        protocol = self.redirect_uri_protocol
        return build_absolute_uri(request, callback_url, protocol)

    def complete_login(self, request, app, token, **kwargs):
        openid = kwargs.get("response", {}).get("openid")
        resp = requests.get(
            self.profile_url,
            headers ={'Content-Type': 'application/json',
                      'Authorization': f'Bearer {token}',
                      'Accept':'application/json'},
        )
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


class FortyTwoOAuth2ClientMixin(object):
    def get_client(self, request, app):
        callback_url = self.adapter.get_callback_url(request, app)
        provider = self.adapter.get_provider()
        scope = provider.get_scope(request)
        client = FortyTwoOAuth2Client(
            request,
            app.client_id,
            app.secret,
            self.adapter.access_token_method,
            self.adapter.access_token_url,
            callback_url,
            scope,
        )
        print(client)
        return client


class FortyTwoOAuth2LoginView(FortyTwoOAuth2ClientMixin, OAuth2LoginView):
    pass


class FortyTwoOAuth2CallbackView(FortyTwoOAuth2ClientMixin, OAuth2CallbackView):
    def dispatch(self, request, *args, **kwargs):
        # Call the original dispatch method to handle the OAuth2 callback
        response = super().dispatch(request, *args, **kwargs)

        # After successful login, generate JWT tokens
        if self.request.user.is_authenticated:
            refresh = RefreshToken.for_user(self.request.user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            if settings.REST_AUTH['USE_JWT']:
                response.set_cookie(
                    settings.REST_AUTH['JWT_AUTH_COOKIE'],
                    access_token,
                    httponly=False,
                    secure=True,
                    samesite='Lax',
                    max_age=access_token_lifetime.total_seconds(),
                )
                response.set_cookie(
                    settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE'],
                    refresh_token,
                    httponly=False,
                    secure=True,
                    samesite='Lax',
                    max_age=refresh_token_lifetime.total_seconds()
                )
            
            return response
        
        return response


oauth2_login = FortyTwoOAuth2LoginView.adapter_view(FortyTwoOAuth2Adapter)
oauth2_callback = FortyTwoOAuth2CallbackView.adapter_view(FortyTwoOAuth2Adapter)