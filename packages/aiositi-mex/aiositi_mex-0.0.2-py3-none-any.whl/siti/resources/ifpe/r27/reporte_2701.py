from typing import Any, Dict, List, Optional

from pydantic import root_validator

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionReclamacion(Resource):
    # _date_format = '%Y-%m-%d'

    folio_reclamacion: Optional[str]
    estatus_reclamacion: Optional[str]
    fecha_actualizacion_estatus: Optional[str]

    @root_validator(pre=True)
    def validate_fields(cls, values: Dict[str, Any]) -> Dict:
        values['folio_reclamacion'] = values['folio_reclamacion'].upper()
        return values


class IdentificadorClienteCuentaMovimiento(Resource):
    identificador_cliente: Optional[str]
    identificador_cuenta: Optional[str]
    identificador_movimiento: Optional[str]


class DetalleReclamacion(Resource):
    fecha_reclamacion: Optional[str]
    canal_recepcion_reclamacion: Optional[str]
    tipo_reclamacion: Optional[str]
    motivo_reclamacion: Optional[str]
    descripcion_reclamacion: Optional[str]


class DetalleEventoOriginaReclamacion(Resource):
    fecha_evento: Optional[str]
    objeto_evento: Optional[str]
    canal_operacion: Optional[str]
    importe_valorizado_moneda_nacional: Optional[str]


class EventosSubsecuentes(Resource):
    detalle_evento_origina_reclamacion: Optional[
        DetalleEventoOriginaReclamacion
    ]


class DetalleResolucion(Resource):
    fecha_resolucion: Optional[str]
    sentido_resolucion: Optional[str]
    importe_abonado_cuenta_cliente: Optional[str]
    fecha_abono_cuenta_cliente: Optional[str]
    identificador_cuenta_fideicomiso_institucion: Optional[str]
    importe_recuperado: Optional[float]
    fecha_recuperacion_recursos: Optional[str]
    identificador_cuenta_recibe_importe_recuperado: Optional[str]
    quebranto_institucion: Optional[str]


class InformacionSolicitada(Resource):
    identificacion_reclamacion: Optional[IdentificacionReclamacion]
    identificador_cliente_cuenta_movimiento: Optional[
        IdentificadorClienteCuentaMovimiento
    ]  # noqa: E501
    detalle_reclamacion: Optional[DetalleReclamacion]
    detalle_evento_origina_reclamacion: Optional[
        DetalleEventoOriginaReclamacion
    ]
    eventos_subsecuentes: Optional[List[EventosSubsecuentes]]
    detalle_resolucion: Optional[DetalleResolucion]

    @root_validator(pre=True)
    def validate_fields(cls, values: Dict[str, Any]) -> Dict:
        # el campo de eventos_subsecuentes solo se debe de mandar en
        # cierto tipo de transacción, por lo que hay que eliminarlo cuando
        # no sea necesario, y de igual manera por eso se sobreescribe el
        # método dict()
        eventos_subsecuentes = values.get('eventos_subsecuentes', [])
        for index, element in enumerate(eventos_subsecuentes):
            if not element:
                eventos_subsecuentes.pop(index)
        if not eventos_subsecuentes:
            eventos_subsecuentes = None
        detalle_reclamacion = values.get('detalle_reclamacion')
        if detalle_reclamacion:
            if detalle_reclamacion.tipo_reclamacion == '302':
                values['eventos_subsecuentes'] = [
                    {
                        'detalle_evento_origina_reclamacion': values[
                            'detalle_evento_origina_reclamacion'
                        ]
                    }
                ]
                values['detalle_reclamacion'] = None
            else:
                values['eventos_subsecuentes'] = []
        iccm = values.get('identificador_cliente_cuenta_movimiento')
        if iccm:
            values[
                'identificador_cliente_cuenta_movimiento'
            ].identificador_cliente = iccm.identificador_cliente.upper()
        detalle_resolucion = values.get('detalle_resolucion')
        if not detalle_resolucion:
            detalle_resolucion = None
        return values

    def dict(self, to_camel_case: bool = False, *args, **kwargs):
        d = super().dict(to_camel_case, *args, **kwargs)
        if not d['eventos_subsecuentes']:
            del d['eventos_subsecuentes']
        return d


class Reporte2701(ReportIFPE, Sendable, Resendable, Updateable):
    """
    En este reporte se recaba información referente a las reclamaciones
    relativas a operaciones con fondos de pago electrónico realizadas
    por los Clientes, agrupadas por productos y canales transaccionales
    de las Instituciones de Fondos de Pago Electrónico. Adicionalmente,
    este reporte considera información respecto de los datos de la
    gestión de dichas reclamaciones.
    """

    _resource = '/IFPE/R27/2701'
    _exclude_from_dataframe = ['eventos_subsecuentes']

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        url = f'{self._endpoint}{self._resource}'
        if not self.informacion_solicitada:
            url = f'{url}/envio-vacio'
        return await super().send(url=url, session=session, **data)
