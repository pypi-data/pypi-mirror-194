from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinancieraBase


class Reporte13221(ReportIFPE, Resendable, Sendable, Updateable):
    """
    Es estado de resultado integral tiene por objetivo mostrar información
    relativa al resultado de sus operaciones en el capital contable y,
    por ende, de los ingresos y gastos y otros resultados integrales (ORI)
    y resultado integral.
    En este reporte se solicita la información relevante sobre las
    operaciones realizadas por la Institución de Fondos de Pago Electrónico
    y deberá cumplir con el objetivo de ser una herramienta útil para el
    análisis.
    """

    _resource = '/IFPE/R13/13221'

    informacion_financiera: conlist(  # type: ignore[valid-type]
        InformacionFinancieraBase, min_items=1
    )
