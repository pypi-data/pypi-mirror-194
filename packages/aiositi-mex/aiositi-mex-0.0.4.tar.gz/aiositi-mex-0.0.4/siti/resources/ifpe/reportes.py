from typing import Optional

from ...http import session
from .base import ResourceIFPE


class Reporte(ResourceIFPE):
    clave_serie: str
    titulo_serie: str
    clave_reporte: str
    titulo_reporte: str
    fecha_inicio: str
    fecha_fin: str
    fecha_inicio_entrega: str
    fecha_fin_entrega: str
    envio_vacio: Optional[str]

    @classmethod
    async def pendientes(cls):
        endpoint = cls._endpoint + '/reporte/pendientes'
        res = await session.get(endpoint)
        txns = [
            cls.from_dict(txn, from_camel_case=True)
            for txn in res['reportePendienteList']
        ]
        return txns
