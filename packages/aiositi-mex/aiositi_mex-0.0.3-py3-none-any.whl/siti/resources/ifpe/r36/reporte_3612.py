from pydantic import conlist

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class Sobregiros(Resource):
    numero_sobregiros_otorgados_periodo: int
    monto_sobregiros_otorgados_periodo: int
    monto_minimo_sobregiros_otorgados_periodo: int
    monto_maximo_sobregiros_otorgados_periodo: int


class CobroSobregiros(Resource):
    saldo_inicio_periodo_sobregiros_cobrar: int
    saldo_final_periodo_sobregiros_cobrar: int
    monto_sobregiros_cobrados_periodo_reportado: int


class InformacionSolicitada(Resource):
    sobregiros: Sobregiros
    cobro_sobregiros: CobroSobregiros


class Reporte3612(ReportIFPE, Resendable, Sendable, Updateable):
    """
    En este reporte se recaba información correspondiente a los
    sobregiros que otorgan las Instituciones de Fondos de Pago Electrónico.
    """

    _resource = '/IFPE/R26/3612'

    informacion_solicitada: conlist(  # type: ignore[valid-type]
        InformacionSolicitada, min_items=1
    )
