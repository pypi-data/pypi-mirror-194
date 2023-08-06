import datetime as dt
import os
from typing import Optional

from pydantic import Field

from ...http import Session, session as global_session
from ..base import Resource

SITI_DEMO = os.getenv('SITI_DEMO', 'false').lower() == 'true'


class ResourceIFPE(Resource):
    _endpoint: str = (
        '/suptech-api/ifpe/1.0.0' if SITI_DEMO else '/suptech-api/IFPE/1.0.0'
    )
    _resource: str
    folio: Optional[str] = None

    _excluded = ['folio']


class IdentificadorReporte(Resource):
    inicio_periodo: dt.date
    fin_periodo: dt.date
    clave_institucion: str = Field(..., min_length=6, max_length=6)
    # check how to assign this field automatically
    reporte: str = Field(..., min_length=3, max_length=5)


class ReportIFPE(ResourceIFPE):
    identificador_reporte: IdentificadorReporte


class Sendable(ResourceIFPE):
    async def send(self, *, url='', session: Session = global_session, **data):
        url = url or f'{self._endpoint}{self._resource}'
        resp = await session.post(
            url,
            self.dict(to_camel_case=True, exclude_none=True),
            **data,
        )
        return resp


class Updateable(ResourceIFPE):
    async def update(self, *, session: Session = global_session, **data):
        resp = await session.put(
            f'{self._endpoint}{self._resource}/correccion/{self.folio}',
            self.dict(to_camel_case=True, exclude_none=True),
            **data,
        )
        return resp


class Resendable(ResourceIFPE):
    async def resend(self, *, session: Session = global_session, **data):
        resp = await session.put(
            f'{self._endpoint}{self._resource}/reenvio/{self.folio}',
            self.dict(to_camel_case=True, exclude_none=True),
            **data,
        )
        # skipping this line because at the moment we do not have
        # a way to resend a report
        return resp  # pragma: no cover
