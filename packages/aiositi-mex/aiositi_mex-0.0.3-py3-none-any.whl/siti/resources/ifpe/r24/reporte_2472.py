import datetime as dt

from pydantic import conlist

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionCliente(Resource):
    identificador_cliente: str


class IdentificacionCuenta(Resource):
    identificador_cuenta: str
    estatus_cuenta: str


class AltaCuentaCliente(Resource):
    fecha_apertura_cuenta: dt.date
    nivel_cuenta: str
    tipo_moneda: str


class CuentasNoActivas(Resource):
    fecha_ultimo_movimiento_cuenta_cliente: dt.date
    fecha_trasppaso_saldo_cliente: dt.date
    fecha_aviso_cliente: dt.date
    fecha_traspaso_beneficencia_publica: dt.date


class Cancelacion(Resource):
    tipo_cancelacion: str
    fecha_cancelacion: dt.date


class InformacionSolicitada(Resource):
    identificacion_cliente: IdentificacionCliente
    identificacion_cuenta: IdentificacionCuenta
    alta_cuentas_cliente: AltaCuentaCliente
    cuentas_no_activas: CuentasNoActivas
    cancelacion: Cancelacion


class Reporte2472(ReportIFPE, Resendable, Sendable, Updateable):
    """
    En este reporte se recaba información que permite conocer
    detalles de la(s) cuenta(s) de los clientes de las IFPE.
    """

    _resource = '/IFPE/R24/2472'

    informacion_solicitada: conlist(  # type: ignore[valid-type]
        InformacionSolicitada, min_items=1
    )
