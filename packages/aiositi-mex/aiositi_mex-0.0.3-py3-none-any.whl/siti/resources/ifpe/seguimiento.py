from ...http import session
from .base import ResourceIFPE


class Seguimiento(ResourceIFPE):
    @classmethod
    async def get(cls, folio_envio: str):
        result = await session.get(
            cls._endpoint + '/seguimiento/' + folio_envio
        )
        return result
