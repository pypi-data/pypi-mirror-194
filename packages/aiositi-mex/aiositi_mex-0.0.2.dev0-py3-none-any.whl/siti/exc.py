class SitiError(Exception):
    """
    Exceptions returned by the SITI API
    """

    code: str
    desc: str

    def __init__(
        self, code: str = None, desc: str = None, *args: object
    ) -> None:
        super().__init__(*args)
        if code:
            self.code = code
        if desc:
            self.desc = desc

    def __str__(self) -> str:
        return self.desc


class InvalidCredentials(SitiError):
    """
    Invalid OAuth credentials
    """


class DateFormatError(SitiError):
    code = 'CLV_ERR_LFNSPP'
    desc = 'Las fechas no se pueden procesar.'


class UserNotFound(SitiError):
    code = 'CLV_ERR_NEEUIRE'
    desc = 'No existe el usuario con el que intenta realizar el envío.'


class DuplicateReport(SitiError):
    code = 'CLV_ERR_SHEOECPS'
    desc = (
        'Se ha encontrado otro envió correspondiente al periodo '
        'solicitado por lo que no se puede recibir otro igual.'
    )


class ReportNotFound(SitiError):
    code = 'CLV_ERR_NECRIRE'
    desc = (
        'No existe la clave del reporte con el que intenta realizar el envío.'
    )


class VersionNotFound(SitiError):
    code = 'CLV_ERR_NEVRP'
    desc = (
        'No existe una versión del reporte en el periodo con el '
        'que intenta realizar el envío.'
    )


class PeriodNotFound(SitiError):
    code = 'CLV_ERR_NEPR'
    desc = 'No existe el periodo que reporta.'


class PeriodNotStarted(SitiError):
    code = 'CLV_ERR_PENC'
    desc = 'El periodo de entrega aún no ha comenzado.'


class StructureError(SitiError):
    code = 'CLV_ERR_ESTR'
    desc = 'Error de estructura.'


class IndexNotFound(SitiError):
    code = 'CLV_ERR_IDNEX'
    desc = 'El folio no existe, verifique el dato y vuelva a intentarlo.'


class UnauthorizedInstitution(SitiError):
    code = 'CLV_ERR_SINTAUT'
    desc = 'Su institución no tiene autorización para usar ese folio.'


class DifferentDates(SitiError):
    code = 'CLV_ERR_FIFFNC'
    desc = 'La fecha de inicio y fin de periodo deben ser iguales.'


class NotTaggedForCorrection(SitiError):
    code = 'CLV_ERR_RNPREEC'
    desc = (
        'El reenvío no puede realizarse ya que el estado de el '
        'envío original no es \'Etiquetado para corrección\''
    )


class NotTaggedForResend(SitiError):
    code = 'CLV_ERR_RNPREE'
    desc = (
        'El reenvío no puede realizarse ya que el estado de el '
        'envío original no es \'Etiquetado para reenvío\''
    )


ERROR_CODES = {
    exc.code: exc
    for exc in [
        DateFormatError,
        UserNotFound,
        DuplicateReport,
        ReportNotFound,
        VersionNotFound,
        PeriodNotFound,
        PeriodNotStarted,
        StructureError,
        IndexNotFound,
        UnauthorizedInstitution,
        DifferentDates,
        NotTaggedForCorrection,
        NotTaggedForResend,
    ]
}
