from typing import List, Optional

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificadorComisionista(Resource):
    identificador_comisionista: str


class IdentificadorModuloEstablecimiento(Resource):
    tipo_movimiento: str
    clave_modulo_establecimiento: str
    rfc_modulo_establecimiento: str
    clave_localidad_modulo_establecimiento: Optional[str]
    clave_estado_modulo_establecimiento: Optional[str]
    clave_municipio_moldulo_establecimiento: Optional[str]  # la api dice moldulo
    codigo_postal_modulo_establecimiento: Optional[str]
    latitud_ubicacion_modulo_establecimiento: Optional[str]
    longitud_ubicacion_modulo_establecimiento: Optional[str]


class BajaModuloEstablecimiento(Resource):
    causa_baja_modulo_establecimiento: str


class InformacionSolicitada(Resource):
    identificador_comisionista: IdentificadorComisionista
    identificador_modulo_establecimiento: IdentificadorModuloEstablecimiento
    baja_modulo_establecimiento: Optional[BajaModuloEstablecimiento]


class Reporte2612(ReportIFPE, Sendable, Updateable, Resendable):
    """
    Este reporte recaba información referente a los módulos o
    establecimientos que los comisionistas bancarios y cambiarios
    tengan habilitados para representar a las propias Instituciones
    de Fondos de Pago Electrónico con sus clientes y con el público
    en general, reportando a la CNBV los movimientos de altas,
    bajas y/o actualizaciones de dichos módulos o establecimientos.
    """

    _resource = '/IFPE/R26/2612'
    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        url = f'{self._endpoint}{self._resource}'
        if not self.informacion_solicitada:
            url = f'{url}/envio-vacio'
        return await super().send(url=url, session=session, **data)
