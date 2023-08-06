from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinanciera


class Reporte13161(ReportIFPE, Resendable, Sendable, Updateable):
    """
    El estado de flujos de efectivo tiene como objetivo principal
    proporcionar información acerca de los cambios en los recursos y
    las fuentes de financiamiento en el periodo contable. Los
    cambios se refieren a las diferencias clasificadas de acuerdo
    a los recursos generados o utilizados por la operación, por
    actividades de financiamiento y por actividades de inversión.
    Asimismo, deberá reflejarse el aumento o disminución de efectivo
    y equivalentes en el periodo.
    """

    _resource = '/IFPE/R13/13161'

    informacion_financiera: conlist(  # type: ignore[valid-type]
        InformacionFinanciera, min_items=1
    )
