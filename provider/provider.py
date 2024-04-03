from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class FortyTwoAccount(ProviderAccount):
    def get_avatar_url(self):
        return self.account.extra_data.get("avatar_big")

    def to_str(self):
        return self.account.extra_data.get(
            "name", super(FortyTwoAccount, self).to_str()
        )


class FortyTwoProvider(OAuth2Provider):
    id = "42"
    name = "42"
    account_class = FortyTwoAccount

    def extract_uid(self, data):
        return data["open_id"]

    def extract_common_fields(self, data):
        return dict(username=data.get("name"), name=data.get("name"))


provider_classes = [FortyTwoProvider]