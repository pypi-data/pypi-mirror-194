import datetime as dt
from typing import List, Optional, Union

from ...http import session
from .base import ResourceIFPE


class MensajeDetail(ResourceIFPE):
    clave: str
    descripcion_corta: str
    descripcion_larga: str


class CatalogoMensajes(ResourceIFPE):
    nombre_catalogo: str
    fecha_creacion: str
    version: str
    item_list: List[MensajeDetail]


class ReporteFechaDetail(ResourceIFPE):
    clave: Optional[str] = None
    descripcion: Optional[str] = None
    concepto: Optional[str] = None
    requerido: Optional[str] = None
    signo: Optional[str] = None
    operacion: Optional[str] = None
    padre: Optional[str] = None


class CatalogoReporteFecha(ResourceIFPE):
    nombre_catalogo: str
    campo: str
    item_list: List[ReporteFechaDetail]


class Catalogo(ResourceIFPE):
    catalogo_list: List[Union[CatalogoMensajes, CatalogoReporteFecha]]

    @classmethod
    async def mensajes(cls):
        endpoint = cls._endpoint + '/catalogo/mensaje-envio'
        res = await session.get(endpoint)
        msgs = [
            CatalogoMensajes.from_dict(msg, from_camel_case=True)
            for msg in res['catalogoList']
        ]
        return cls(catalogo_list=msgs)

    @classmethod
    async def reporte_fecha(
        cls, clave_reporte: str, inicio_periodo: dt.date, fin_periodo: dt.date
    ):
        inicio = inicio_periodo.strftime('%Y-%m-%d')
        final = fin_periodo.strftime('%Y-%m-%d')
        endpoint = (
            cls._endpoint + f'/catalogo/{clave_reporte}/{inicio}/{final}'
        )
        res = await session.get(endpoint)
        msgs = [
            CatalogoReporteFecha.from_dict(msg, from_camel_case=True)
            for msg in res['catalogoList']
        ]
        return cls(catalogo_list=msgs)
