from pydantic import Field, conlist

from ...base import REGEX_NUMERIC, Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class InformacionFinanciera(Resource):
    concepto: str = Field(
        ..., min_length=12, max_length=12, regex=REGEX_NUMERIC
    )
    moneda: str = Field(..., max_length=2, regex=REGEX_NUMERIC)
    dato: float


class Reporte111(ReportIFPE, Sendable, Updateable, Resendable):
    """
    En este reporte se solicitan los saldos al cierre del período
    de todos los conceptos que forman parte del estado de situación
    financiera (incluyendo las cuentas de orden) y del estado de
    resultado integral de la Institución de Fondos de Pago Electrónico.
    """

    _resource = '/IFPE/R01/111'

    informacion_financiera: conlist(  # type: ignore[valid-type]
        InformacionFinanciera, min_items=1
    )
