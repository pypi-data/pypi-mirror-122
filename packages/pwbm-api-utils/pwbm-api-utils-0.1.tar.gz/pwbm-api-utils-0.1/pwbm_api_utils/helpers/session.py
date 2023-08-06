from functools import wraps
from urllib.parse import urljoin

import requests
import requests.adapters

from pwbm_api_utils.constants import APIEnvs, ENV_DATA


def get_access_token(client_id: str, user: str, password: str):
    r = requests.post(
        url='https://cognito-idp.us-east-2.amazonaws.com/',
        headers={
            'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth',
            'Content-Type': 'application/x-amz-json-1.1',
        },
        json={
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": client_id,
            "AuthParameters": {
                "USERNAME": user,
                "PASSWORD": password,
            },
            "ClientMetadata": {},
        },
    )
    r.raise_for_status()
    return r.json()['AuthenticationResult']['AccessToken']


class Session(requests.Session):
    __attrs__ = ['base_url', *requests.Session.__attrs__]

    @wraps(requests.Session.__init__)
    def __init__(self, *args, base_url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    @wraps(requests.Session.request)
    def request(self, method, url, **kwargs):
        modified_url = urljoin(self.base_url, url)
        return super().request(method, modified_url, **kwargs)


def get_session(env: APIEnvs, user: str, password: str) -> Session:
    auth_token = get_access_token(ENV_DATA[env]['cognito_client_id'], user, password)
    session = Session(base_url=ENV_DATA[env]['api_prefix'])
    session.headers.update({
        'Authorization': f'Bearer {auth_token}',
    })
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)  # FixMe
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
