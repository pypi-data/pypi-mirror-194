from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinancieraBase


class Reporte13211(ReportIFPE, Resendable, Sendable, Updateable):
    """
    El estado de situación financiera tiene por objetivo presentar
    el valor de los bienes y derechos, de las obligaciones reales,
    directas o contingentes, así como del capital contable de la
    Institución de Fondos de Pago Electrónico a una fecha determinada.
    El estado de situación financiera, por lo tanto, deberá mostrar
    de manera adecuada y sobre bases consistentes, la posición de la
    institución en cuanto a sus activos, pasivos, capital contable y
    cuentas de orden, de tal forma que se puedan evaluar los recursos
    económicos con que cuenta la institución, así como su estructura
    financiera.
    Adicionalmente, el estado de situación financiera deberá cumplir
    con el objetivo de ser una herramienta útil para el análisis.
    """

    _resource = '/IFPE/R13/13211'

    informacion_financiera: conlist(  # type: ignore[valid-type]
        InformacionFinancieraBase, min_items=1
    )
