from ..base import Resource


class InformacionFinancieraBase(Resource):
    concepto: str
    dato: float


class InformacionFinanciera(Resource):
    concepto: str
    tipo_saldo: str
    dato: float
