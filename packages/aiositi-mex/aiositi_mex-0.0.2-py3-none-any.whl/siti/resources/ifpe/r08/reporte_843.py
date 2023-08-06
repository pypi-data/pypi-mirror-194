import datetime as dt
from typing import List, Optional

from pydantic import Field

from ....http import Session, session as global_session
from ...base import REGEX_CAP_NUM, REGEX_NUMERIC, Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable
from ..types import (
    EstatusPrestamo,
    PeriodicidadPagosCapital,
    TipoDisposicionCredito,
    TipoGarantia,
    TipoPrestamista,
    TipoPrestamo,
    TipoTasaInteres,
)


class IdentificarPrestamo(Resource):
    identificador_prestamo: str = Field(
        ..., max_length=50, regex=REGEX_CAP_NUM
    )
    estatus_prestamo: EstatusPrestamo
    fecha_actualizacion_estatus: dt.date


class DatosIdentificacionPrestamista(Resource):
    tipo_prestamista: TipoPrestamista
    nombre_razon_denominacion_social: str = Field(
        ...,
        max_length=200,
    )
    apellido_paterno: str = Field(..., max_length=60)
    apellido_materno: str = Field(..., max_length=60)
    pais_origen: str = Field(..., max_length=3, regex=REGEX_NUMERIC)


class DatosCuenta(Resource):
    identificador_cuenta: str = Field(..., max_length=21, regex=REGEX_NUMERIC)


class DatosOperacion(Resource):
    clasificacion_contable: TipoPrestamo
    fecha_contratacion_apertura: dt.date
    fecha_vencimiento: dt.date
    periodicidad_pagos_capital: PeriodicidadPagosCapital
    periodicidad_pagos_interes: str
    tipo_moneda: str
    monto_inicial_prestamo_moneda_origen: float
    monto_inicial_prestamo_valorizado_moneda_nacional: float
    tipo_cambio: float
    tipo_tasa_interes: TipoTasaInteres
    valor_tasa_originalmente_pactada: str
    valor_tasa_interes_aplicable_periodo: float
    tasa_interes_referencia: str
    ajuste_tasa_referencia: str
    frecuencia_revision_tasa: int
    importe_comision_pactada: float
    tipo_disposicion_credito: TipoDisposicionCredito
    destino_recursos: str


class DatosSeguimientoPrestamo(Resource):
    _date_format = '%Y-%m-%d'

    saldo_insoluto_inicio_periodo: float
    capital_exigible: float
    intereses_exigibles: float
    pagos_capital: float
    interese_pagados: float
    otras_comisiones_pagadas: float
    intereses_devengados_no_pagados: float
    saldoinsoluto_cierre_periodo: float
    porcentaje_dispuesto_credito: int
    fecha_ultimo_pago_realizado: dt.date
    fecha_pago_inmediato_siguiente: dt.date
    monto_pago_inmediato_siguiente: float


class DatosIdentificacionGarantiasPrestamo(Resource):
    _date_format = '%Y-%m-%d'

    tipo_garantia: TipoGarantia
    valor_inicial: float
    valor_actualizado: float
    fecha_evaluacion: dt.date


class InformacionSolicitada(Resource):
    identificar_prestamo: IdentificarPrestamo
    datos_identificacion_prestamista: DatosIdentificacionPrestamista
    datos_cuenta: DatosCuenta
    datos_operacion: DatosOperacion
    datos_seguimiento_prestamo: DatosSeguimientoPrestamo
    datos_identificacion_garantias_prestamo: DatosIdentificacionGarantiasPrestamo  # noqa: E501


class Reporte843(ReportIFPE, Sendable, Updateable, Resendable):
    """
    En este reporte se recaba información que permite conocer el detalle
    de los préstamos otorgados a las Instituciones de Fondos de Pago
    Electrónico, tales como la fecha de contratación del crédito, la
    fecha de vencimiento, el monto de la operación, la tasa de interés
    pactada, las garantías que lo respaldan, la identificación del
    prestamista, las comisiones pagadas, entre otros,
    así como la información del seguimiento del crédito.
    """

    _resource = '/IFPE/R08/843'

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        url = f'{self._endpoint}{self._resource}'
        if not self.informacion_solicitada:
            url = f'{url}/envio-vacio'
        return await super().send(url=url, session=session, **data)
