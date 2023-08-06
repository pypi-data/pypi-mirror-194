from typing import List, Optional

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionAdministrador(Resource):
    identificador_administrador: str
    tipo_movimiento: str
    nombre_administrador: str
    rfc_administrador: Optional[str]
    personalidad_juridica_administrador: Optional[str]
    modalidad_comercial_administrador: Optional[str]
    nombre_comercial: Optional[str]


class BajaAdministrador(Resource):
    causa_baja_administrador: str


class InformacionSolicitada(Resource):
    identificacion_administrador: IdentificacionAdministrador
    baja_administrador: BajaAdministrador


class Reporte2610(ReportIFPE, Sendable, Updateable, Resendable):
    """
    Este reporte recaba información referente a los movimientos
    de Altas y/o Bajas de los Administradores de Comisionistas,
    que sean contratados por la Institución de Fondos de Pago
    Electrónico para que sean intermediarios entre los comisionistas
    y la Institución.
    """

    _resource = '/IFPE/R26/2610'

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        url = f'{self._endpoint}{self._resource}'
        if not self.informacion_solicitada:
            url = f'{url}/envio-vacio'
        return await super().send(url=url, session=session, **data)
