import base64
import datetime as dt
from dataclasses import dataclass

import requests

from ..exc import InvalidCredentials

EXPIRATION_TIME = 3600


@dataclass
class OAuthToken:
    expires_at: dt.datetime
    token: str

    @property
    def is_expired(self) -> bool:
        return self.expires_at <= dt.datetime.utcnow()

    @classmethod
    def create(cls, base_url: str, consumer_key: str, consumer_secret: str):
        url = f'{base_url}/token'
        data = dict(grant_type='client_credentials')
        creds = base64.b64encode(
            f'{consumer_key}:{consumer_secret}'.encode()
        ).decode()
        headers = dict(Authorization=f'Basic {creds}')
        # using requests instead of aiohttp so this method is
        # not async and can be used in the __init__ function.
        res = requests.post(url, data=data, headers=headers)
        if not res.ok:
            raise InvalidCredentials('Error', res.json()['error_description'])
        response = res.json()
        oauth_token = response['access_token']
        expires_at = dt.datetime.utcnow() + dt.timedelta(
            seconds=response['expires_in']
        )
        return cls(expires_at, oauth_token)
