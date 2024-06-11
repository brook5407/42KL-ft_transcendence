import requests
import json
from django.conf import settings
from collections import OrderedDict
from urllib.parse import quote, urlencode
from django.utils.http import urlencode

from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Client,
    OAuth2Error,
)

class FortyTwoOAuth2Client(OAuth2Client):

    base_url = f'{settings.FT_OAUTH_SERVER_BASE_URL}/oauth/authorize'
    token_url = f'{settings.FT_OAUTH_SERVER_BASE_URL}/oauth/token'
    redirect_uri = 'http://127.0.0.1:8000/42/login/callback/'
    response_type = 'code'
    
    def get_redirect_url(self, authorization_url, extra_params):
        
        params = {
            'client_id': self.consumer_key,
            'redirect_uri': self.callback_url,
            'response_type': self.response_type,
        }
        if self.state:
            params["state"] = self.state
        params.update(extra_params)
        return "%s?%s" % (authorization_url, urlencode(params))

    def get_access_token(self, code, pkce_code_verifier=None):
        """
        Request access token from the provider using the code returned by the
        Returns:
            {
                "access_token": "cf04dea4652cac698153b0a33321f97ec60103f38af469ac86586ca13b962fc7",
                "token_type": "bearer",
                "expires_in": 7200,
                "scope": "public",
                "created_at": 1712043465,
                "secret_valid_until": 1714314643
            }
        """

        data = {
            "grant_type": "authorization_code",
            "client_id": self.consumer_key,
            "client_secret": self.consumer_secret,
            "code": code,
            "redirect_uri": self.callback_url
        }
        params = None
        self._strip_empty_keys(data)
        url = self.access_token_url
        if self.access_token_method == "GET":
            params = data
            data = None

        resp = requests.request(self.access_token_method, url, params=params, 
                                data=json.dumps(data), headers={'Content-Type': 'application/json'})
        access_token = None
        if resp.status_code == 200:
            access_token = resp.json()
        else:
            raise OAuth2Error("Error retrieving app access token: %s" % resp.content)
        
        return access_token
