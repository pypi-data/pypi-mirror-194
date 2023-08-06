from pydantic import conlist

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionClienteCuenta(Resource):
    identificador_cliente: str
    identificador_cuenta: str


class Saldos(Resource):
    saldo_inicio_periodo_moneda_origen: float
    saldo_inicial_valorizado_moneda_nacional: float
    saldo_final_periodo_moneda_origen: float
    saldo_final_valorizado_moneda_nacional: float
    tipo_moneda: str
    tipo_cambio: float


class MovimientosSobregirosAgregadosCuenta(Resource):
    numero_total_movimientos: int
    numero_total_movimientos_cargo: int
    saldo_total_movimientos_cargo: float
    numero_total_movimientos_abono: int
    saldo_total_movimientos_abono: float
    numero_total_movimientos_moneda_nacional: int
    numero_total_movimientos_cargo_moneda_nacional: int
    saldo_total_movimientos_cargo_moneda_nacional: float
    numero_total_movimientos_abono_moneda_nacional: int
    saldo_total_movimientos_abono_moneda_nacional: float
    numero_total_movimientos_moneda_extranjera: int
    numero_total_movimientos_cargo_moneda_extranjera: int
    saldo_total_movimientos_cargo_moneda_extranjera: float
    numero_total_movimientos_abono_moneda_extranjera: int
    saldo_total_movimientos_abono_moneda_extranjera: float
    numero_total_movimientos_efectivo: int
    numero_movimientos_cargo_efectivo: int
    saldo_movimientos_cargo_efectivo: int
    numero_movimientos_abono_efectivo: int
    saldo_movimientos_abono_efectivo: int
    saldo_movimientos_cargo_tarjeta: float
    saldo_movimientos_abono_cheque: int
    saldo_movimientos_cargo_transferencia_entidad_financiera_nacional: float
    saldo_movimientos_abono_transferencia_entidad_financiera_nacional: float
    saldo_movimientos_cargo_transferencia_entidad_financiera_exterior: float
    saldo_movimientos_abono_transferencia_entidad_financiera_exterior: float
    saldo_movimientos_cargo_transferencia_i_f_p_e: float
    saldo_movimientos_abono_transferencia_i_f_p_e: float
    numero_sobregiros_otorgados: int
    saldo_sobregiros_otorgados: float
    saldo_sobregiros_cobrados: float
    monto_minimo_abono: float
    monto_minimo_cargo: float
    monto_maximo_abono: int
    monto_maximo_cargo: float
    saldo_comisiones_cobradas: float


class InformacionSolicitada(Resource):
    identificacion_cliente_cuenta: IdentificacionClienteCuenta
    saldos: Saldos
    movimientos_sobregiros_agregados_cuenta: MovimientosSobregirosAgregadosCuenta  # noqa: 501


class Reporte3611(ReportIFPE, Resendable, Sendable, Updateable):
    """
    En este reporte se recaba información referente a los números y
    saldos de los movimientos de cargos y abonos realizados en moneda
    nacional o extranjera en las cuentas de los clientes de las
    Instituciones de Fondos de Pago Electrónico.
    """

    _resource = '/IFPE/R26/3611'

    informacion_solicitada: conlist(  # type: ignore[valid-type]
        InformacionSolicitada, min_items=1
    )
