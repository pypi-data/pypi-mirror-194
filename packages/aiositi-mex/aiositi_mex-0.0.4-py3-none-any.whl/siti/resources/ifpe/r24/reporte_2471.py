from pydantic import conlist

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionCliente(Resource):
    identificador_cliente: str
    estatus_registro_cliente: str
    fecha_actualizacion_estatus: str


class AltaActualizacionReactivacionCliente(Resource):
    tipo_persona: str
    rfc_cliente: str
    curp_cliente: str
    clasificacion_cliente: str
    nombre_denominacion_social: str
    apellidos_paternos: str
    apellidos_maternos: str
    genero: str
    fecha_nacimiento_constitucion: str
    entidad_federativa_nacimiento_constitucion: str
    pais_nacimiento: str
    nacionalidad: str
    ocupacion: str
    actividad_economica_giro_negocio: str
    nombre_calle_avenida_via: str
    numero_exterior: str
    numero_interior: str
    colonia: str
    codigo_postal: str
    localidad: str
    entidad_federativa: str
    municipio: str
    pais: str
    telefono: str
    correo_electronico: str


class BajaCliente(Resource):
    motivo_baja: str


class InformacionSolicitada(Resource):
    identificacion_cliente: IdentificacionCliente
    alta_actualizacion_reactivacion_cliente: AltaActualizacionReactivacionCliente  # noqa: E501
    baja_cliente: BajaCliente


class Reporte2471(ReportIFPE, Resendable, Sendable, Updateable):
    """
    En este reporte se recaba información de los clientes de las IFPE.
    """

    _resource = '/IFPE/R24/2471'

    informacion_solicitada: conlist(  # type: ignore[valid-type]
        InformacionSolicitada, min_items=1
    )
