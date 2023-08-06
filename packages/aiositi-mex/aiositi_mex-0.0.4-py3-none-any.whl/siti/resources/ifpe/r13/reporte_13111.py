from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinanciera


class Reporte13111(ReportIFPE, Resendable, Sendable, Updateable):
    """
    El estado de cambios en el capital contable tiene por objetivo
    presentar información sobre los cambios en la inversión de los
    propietarios de la Institución de Fondos de Pago Electrónico
    durante el periodo contable. Debe mostrar la conciliación entre
    saldos iniciales y finales del periodo de cada uno de los rubros
    que forman parte del capital contable. En este reporte se
    solicitan los saldos de todos los conceptos del capital contable
    de la Institución de Fondos de Pago Electrónico, mostrando los
    movimientos ocurridos en el período que se reporta. Los movimientos
    se refieren a los incrementos o decrementos del capital contable
    originados por movimientos de propietarios, movimientos de
    reservas y resultado integral.
    """

    _resource = '/IFPE/R13/13111'

    informacion_financiera: conlist(  # type: ignore[valid-type]
        InformacionFinanciera, min_items=1
    )
