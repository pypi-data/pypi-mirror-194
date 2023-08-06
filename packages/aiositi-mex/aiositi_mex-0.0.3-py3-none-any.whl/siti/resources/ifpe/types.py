from enum import Enum


class EstatusPrestamo(Enum):
    alta = '101'
    alta_reestructura = '102'
    reactivacion = '103'
    seguimiento = '104'
    cancelacion = '105'
    liquidacion = '106'
    baja = '107'
    dacion_en_pago = '108'
    actualizacion = '109'


class TipoPrestamista(Enum):
    banca_multiple = '201'
    bancos_extranjeros = '202'
    banca_de_desarrollo = '203'
    fideicomisos_publicos = '204'
    sociedades_financieras_populares = '205'
    sociedades_cooperativas_de_ahorro_y_prestamo = '206'
    gobierno_federal = '207'
    gobierno_estatal = '208'
    otros_organismos = '209'
    otras_entidades_financieras = '210'
    personas_fisicas = '211'
    prestamos_personas_relacionadas = '211'


class TipoPrestamo(Enum):
    prestamo_banca_multiple = '200600103001'
    prestamo_bancos_extranjeros = '200600103002'
    prestamo_banca_de_desarrollo = '200600103003'
    prestamo_fideicomisos_publicos = '200600103004'
    otros_organismos = '200600103005'
    prestamo_banca_multiple_2 = '200600203006'
    prestamo_bancos_extranjeros_2 = '200600203007'
    prestamo_banca_de_desarrollo_2 = '200600203008'
    prestamo_fideicomisos_publicos_2 = '200600203009'
    otros_organismos_2 = '200600203010'


class PeriodicidadPagosCapital(Enum):
    semanal = '301'
    quincenal = '302'
    mensual = '303'
    bimestral = '304'
    trimestral = '305'
    semestral = '306'
    anual = '307'
    unico = '308'
    amortizaciones_irregulares = '309'


class PeriodicidadPagosInterés(Enum):
    semanal = '401'
    quincenal = '402'
    mensual = '403'
    bimestral = '404'
    trimestral = '405'
    semestral = '406'
    anual = '407'
    unico = '408'
    irregulares = '409'


class TipoTasaInteres(Enum):
    fija = '501'
    variable = '502'
    mixta = '503'


class TipoDisposicionCredito(Enum):
    unica = '701'
    diversas_disposiciones = '702'
    revolvente = '703'


class TipoGarantia(Enum):
    dinero_en_efectivo = '801'
    acciones_representativas_de_capital = '802'
    bienes_muebles = '803'
    bienes_inmuebles = '804'
    documentos_por_cobrar = '805'
    garantia_fiduciaria = '806'
    masa_de_garantias = '807'
    sin_garantia = '808'
