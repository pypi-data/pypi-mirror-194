from typing import List, Optional

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionAdministrador(Resource):
    identificador_administrador: str


class IdentificacionComisionista(Resource):
    tipo_movimiento: str
    identificador_comisionista: str
    nombre_comisionista: str
    rfc_comisionista: Optional[str]
    personalidad_juridica_comisionista: Optional[str]
    modalidad_comercial_comisionista: Optional[str]
    nombre_comercial: Optional[str]


class OperacionesContratadasComisionista(Resource):
    operaciones_contratadas: List[str]


class BajaComisionista(Resource):
    causa_baja_comisionista: str


class InformacionSolicitada(Resource):
    identificacion_administrador: IdentificacionAdministrador
    identificacion_comisionista: IdentificacionComisionista
    operaciones_contratadas_comisionista: OperacionesContratadasComisionista
    baja_comisionista: Optional[BajaComisionista]


class Reporte2611(ReportIFPE, Sendable, Updateable, Resendable):
    """
    Este reporte recaba información referente al tipo de servicio y
    operaciones contratadas con los comisionistas, las actualizaciones
    en las condiciones del contrato mercantil y las causas que dan
    origen a la baja del contrato.
    """

    _resource = '/IFPE/R26/2611'

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        url = f'{self._endpoint}{self._resource}'
        if not self.informacion_solicitada:
            url = f'{url}/envio-vacio'
        return await super().send(url=url, session=session, **data)
