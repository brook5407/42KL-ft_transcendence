import os
import requests
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.conf import settings


class FortyTwoAccount(ProviderAccount):
    pass


class FortyTwoProvider(OAuth2Provider):
    id = "42"
    name = "42"
    account_class = FortyTwoAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        print(data)
        return dict(
                    username=data['login'],
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    )

    def extract_email_addresses(self, data):
        ret = []
        email = data.get("email")
        if email:
            # verified = bool(data.get("email_verified") or data.get("verified_email"))
            ret.append(EmailAddress(email=email, verified=True, primary=True))
        return ret

provider_classes = [FortyTwoProvider]