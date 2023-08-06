import os
from typing import Any, Dict, Optional

import aiohttp
from aiohttp.client_reqrep import ClientResponse

from ..exc import ERROR_CODES, SitiError
from .oauth_token import OAuthToken

API_URL = 'https://sitiapi.cnbv.gob.mx:8243'
API_URL_QA = 'https://sitiapiqa.cnbv.gob.mx:8243'

SITI_DEMO = os.getenv('SITI_DEMO', 'false').lower() == 'true'


class Session:
    consumer_key: str
    consumer_secret: str
    base_url: str = API_URL
    oauth_token: Optional[OAuthToken] = None

    _connection_pool_size: int

    def __init__(self) -> None:
        self.consumer_key = os.getenv('SITI_CONSUMER_KEY', '')
        self.consumer_secret = os.getenv('SITI_CONSUMER_SECRET', '')
        self.base_url = API_URL_QA if SITI_DEMO else API_URL
        self._connection_pool_size = 4

    def configure(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        demo: bool = False,
        pool_size: Optional[int] = None,
    ) -> None:
        if consumer_key:
            self.consumer_key = consumer_key
        if consumer_secret:
            self.consumer_secret = consumer_secret
        if demo or SITI_DEMO:
            self.base_url = API_URL_QA
        if pool_size:  # pragma: no cover
            self._connection_pool_size = pool_size

        self.oauth_token = OAuthToken.create(
            self.base_url, self.consumer_key, self.consumer_secret
        )

    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self.request('GET', endpoint, {}, **kwargs)

    async def post(
        self, endpoint: str, data: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]:
        return await self.request('POST', endpoint, data, **kwargs)

    async def put(
        self, endpoint: str, data: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]:
        return await self.request('PUT', endpoint, data, **kwargs)

    async def request(
        self, method: str, endpoint: str, data: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]:
        # if this is the first call or token is expired,
        # it will populate the token
        if not self.oauth_token or self.oauth_token.is_expired:
            self.oauth_token = OAuthToken.create(
                self.base_url, self.consumer_key, self.consumer_secret
            )
        url = self.base_url + endpoint
        # establishing a maximum amount of simultaneous connections for async
        conn = aiohttp.TCPConnector(limit=self._connection_pool_size)
        headers = dict(
            Authorization=f'Bearer {self.oauth_token.token}',  # type: ignore
            accept='application/json',
        )
        async with aiohttp.ClientSession(
            connector=conn, headers=headers
        ) as session:
            async with session.request(
                method,
                url,
                json=data,
                **kwargs,
            ) as response:
                resultado = await response.json()
                await self._check_response(response)
        return resultado

    @classmethod
    async def _check_response(cls, response: ClientResponse) -> None:
        if not response.ok:
            json = await response.json()
            if 'claveError' in json:
                try:
                    raise ERROR_CODES[json['claveError']]
                except KeyError:
                    raise SitiError(
                        code=json['claveError'], desc=json['mensaje']
                    )
            raise SitiError(code='ERROR', desc=json)
