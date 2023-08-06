from typing import List, Optional

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionAdministrador(Resource):
    identificador_administrador: str


class IdentificacionComisionista(Resource):
    identificador_comisionista: str


class IdentificadorModulosEstablecimientos(Resource):
    clave_modulo_establecimiento: str


class InformacionOperativa(Resource):
    numero_modulos_establecimientos_comisionista: int


class ClasificadoresAgrupacion(Resource):
    tipo_operacion_realizada: str
    medio_pago_utilizado: str


class MovimientosOperaciones(Resource):
    numero_operaciones_realizadas_comisionista: int
    monto_operaciones_realizadas_valorizadas_moneda_nacional: float
    numero_clientes_institucion_realizaron_operaciones: int


class InformacionOperaciones(Resource):
    clasificadores_agrupacion: ClasificadoresAgrupacion
    movimientos_operaciones: MovimientosOperaciones


class InformacionSolicitada(Resource):
    identificacion_administrador: IdentificacionAdministrador
    identificacion_comisionista: IdentificacionComisionista
    identificador_modulos_establecimientos: IdentificadorModulosEstablecimientos  # noqa: E501
    informacion_operativa: InformacionOperativa
    informacion_operaciones: List[InformacionOperaciones]


class Reporte2613(ReportIFPE, Sendable, Updateable, Resendable):
    """
    Este reporte permite observar en el tiempo los posibles cambios
    que se presenten en el tipo y número de operaciones contratadas,
    así como conocer los flujos generados, por las operaciones de
    recepción de recursos en efectivo.
    """

    _resource = '/IFPE/R26/2613'

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        url = f'{self._endpoint}{self._resource}'
        if not self.informacion_solicitada:
            url = f'{url}/envio-vacio'
        return await super().send(url=url, session=session, **data)
