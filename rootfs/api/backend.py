from django.conf import settings

from social_core.backends.oauth import BaseOAuth2
from social_core.backends.open_id_connect import OpenIdConnectAuth


class DryccOAuth(BaseOAuth2):
    """Drycc OAuth authentication backend"""
    name = 'drycc'
    AUTHORIZATION_URL = settings.SOCIAL_AUTH_DRYCC_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.SOCIAL_AUTH_DRYCC_ACCESS_TOKEN_URL
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('access_token', 'access_token'),
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires_in'),
        ('token_type', 'token_type'),
        ('id_token', 'id_token'),
        ('scope', 'scope'),
    ]

    def get_user_details(self, response):
        """Return user details from GitHub account"""
        print(response)
        return {
            'username': response.get('username'),
            'email': response.get('email') or '',
            'first_name': response.get('first_name'),
            'last_name': response.get('last_name'),
            'is_superuser': response.get('is_superuser'),
            'is_staff': response.get('is_staff'),
            'is_active': response.get('is_active'),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = settings.SOCIAL_AUTH_DRYCC_ACCESS_API_URL
        return self.get_json(url, headers={
            'authorization': 'Bearer ' + access_token})

    def get_user_id(self, details, response):
        """Use user account id as unique id"""
        return response.get('id')


class DryccOIDC(OpenIdConnectAuth):
    """Drycc Openid Connect authentication backend"""
    name = 'drycc'
    AUTHORIZATION_URL = settings.SOCIAL_AUTH_DRYCC_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.SOCIAL_AUTH_DRYCC_ACCESS_TOKEN_URL
    USERINFO_URL = settings.SOCIAL_AUTH_DRYCC_USERINFO_URL
    JWKS_URI = settings.SOCIAL_AUTH_DRYCC_JWKS_URI
    OIDC_ENDPOINT = settings.SOCIAL_AUTH_DRYCC_OIDC_ENDPOINT
    DEFAULT_SCOPE = ['openid']
    EXTRA_DATA = [
        ('id', 'id'),
        ('access_token', 'access_token'),
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires_in'),
        ('token_type', 'token_type'),
        ('id_token', 'id_token'),
        ('scope', 'scope'),
    ]

    from social_core.utils import cache
    @cache(ttl=86400)
    def oidc_config(self):
        return self.get_json(self.OIDC_ENDPOINT +
                             '/.well-known/openid-configuration/')
