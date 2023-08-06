from pydantic import conlist

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionCuentaFideicomiso(Resource):
    tipo_cuenta: str
    numero_cuetnta_fideicomiso: str
    clave_casfim_entidad_financiera: str
    tipo_moneda: str


class SeguimientoCuentaFideicomiso(Resource):
    saldo_inicio_periodo: float
    saldo_final_periodo: float
    numero_total_abonos_periodo: int
    monto_total_abonos_periodo: int
    importe_maximo_abonos_periodo: int
    monto_total_abonos_efectivo: int
    monto_total_abonos_transferencia_electronica_institucion_fondos_pago_electronico: int  # noqa: 501
    monto_total_abonos_transferencia_electronica_entidad_financiera_nacional: int  # noqa: 501
    monto_total_abonos_transferencia_electronica_entidad_financiera_exterior: int  # noqa: 501
    movimientos_abonos_realizados_atraves_cheques: int
    numero_total_cargos_periodo: int
    monto_total_cargos_periodo: int
    importe_maximo_cargos_periodo: int
    monto_total_cargos_dispuestos_efectivo: int
    monto_total_cargos_tarjeta: int
    monto_total_cargos_transferencia_electronica_institucion_fondos_pago_electronico: int  # noqa: 501
    monto_total_cargos_transferencia_electronica_entidad_financiera_nacional: int  # noqa: 501
    monto_total_cargos_transferencia_electronica_entidad_financiera_exterior: int  # noqa: 501
    monto_total_comisiones_cobradas: int


class InformacionSolicitada(Resource):
    identificacion_cuenta_fideicomiso: IdentificacionCuentaFideicomiso
    seguimiento_cuenta_fideicomiso: SeguimientoCuentaFideicomiso


class Reporte3613(ReportIFPE, Resendable, Sendable, Updateable):
    """
    En este reporte se recaba información correspondiente a detalle
    de las cuentas o fideicomisos que las Instituciones de Fondos de
    Pago Electrónico utilizan para el manejo de los recursos de sus clientes.
    """

    _resource = '/IFPE/R26/36123'

    informacion_solicitada: conlist(  # type: ignore[valid-type]
        InformacionSolicitada, min_items=1
    )
