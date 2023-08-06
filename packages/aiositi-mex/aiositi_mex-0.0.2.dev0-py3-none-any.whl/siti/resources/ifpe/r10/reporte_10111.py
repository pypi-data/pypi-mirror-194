from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinanciera


class Reporte10111(ReportIFPE, Resendable, Sendable, Updateable):
    """
    En este reporte se solicitan saldos al cierre del período
    de los conceptos del reporte regulatorio A-0111 Catálogo mínimo,
    así como los respectivos movimientos por presentación y
    compensaciones conforme a criterios contables realizados para
    fines de presentación de los rubros del estado de situación
    financiera de la Institución de Fondos de Pago Electrónico
    sin consolidar.
    """

    _resource = '/IFPE/R10/10111'

    informacion_financiera: conlist(  # type: ignore[valid-type]
        InformacionFinanciera, min_items=1
    )
