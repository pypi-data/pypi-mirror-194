import datetime as dt
from enum import Enum
from typing import Any, Dict, get_origin

import pandas as pd
from pydantic import BaseModel

from ..utils import dict_to_camel_case, dict_to_snake_case

REGEX_NUMERIC = r'^\d*$'
REGEX_CAP_NUM = r'^[A-Z0-9\-\s]*$'


class Resource(BaseModel):
    _date_format = '%Y%m%d'
    _excluded: list = []
    _exclude_from_dataframe: list = []

    @classmethod
    def from_dict(cls, d: Dict[str, Any], from_camel_case: bool = False):
        if from_camel_case:
            d = dict_to_snake_case(d)
        return cls(**d)

    def dict(self, to_camel_case: bool = False, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        res = {}
        for key, value in d.items():
            if key in self._excluded:
                continue
            if isinstance(value, dt.date) or isinstance(value, dt.datetime):
                res[key] = value.strftime(self._date_format)
            elif isinstance(value, Enum):
                res[key] = value.value
            else:
                res[key] = value
        if to_camel_case:
            res = dict_to_camel_case(res)
            res = res
        return res

    @classmethod
    def from_dataframe(cls, name: str, df: pd.DataFrame):
        """
        el nombre debe de venir en formato:
        CLAVEINSTITUCION_REPORTE_FECHAINICIO_FECHAFINAL.csv
        ejemplo:
        065014_2610_20210831_20210831.csv
        """
        list_field_name = (
            'informacion_solicitada'
            if 'informacion_solicitada' in cls.__fields__
            else 'informacion_financiera'
        )
        list_element_cls = cls.__fields__[list_field_name].type_
        identificador_reporte_cls = cls.__fields__[
            'identificador_reporte'
        ].type_

        elements_for_list = []
        for _, row in df.iterrows():
            elements_for_list.append(list_element_cls._from_series(row))

        name = name.replace('.csv', '')
        name_fields = name.split('_')
        identificador_reporte = identificador_reporte_cls(
            inicio_periodo=dt.datetime.strptime(name_fields[2], '%Y%m%d'),
            fin_periodo=dt.datetime.strptime(name_fields[3], '%Y%m%d'),
            clave_institucion=name_fields[0],
            reporte=name_fields[1],
        )

        obj = {
            list_field_name: elements_for_list,
            'identificador_reporte': identificador_reporte,
        }

        return cls(**obj)

    @classmethod
    def _from_series(cls, row: pd.Series):
        obj = dict()
        for k, v in cls.__fields__.items():
            if k in cls._exclude_from_dataframe:
                continue
            # esto se hace para que cuando sea una lista
            # se logre iterar por todos sus elementos
            if issubclass(get_origin(v.outer_type_) or v.outer_type_, list):
                if issubclass(v.type_, BaseModel):
                    # por ahora solo acepta listas de un solo elemento
                    # hay que definir bien con Dani como ponerlo en el csv
                    obj[k] = [v.type_._from_series(row)]
                else:
                    # este es para cuando se pasa una cadena de texto
                    # con varios elementos separados por comas
                    obj[k] = row[v.name].split(',')
            elif issubclass(v.type_, BaseModel):
                # recursivo
                obj[k] = v.type_._from_series(row)
            elif row[v.name] is None or row[v.name] == '':
                # esto se hace cuando el elemento viene vacío
                obj[k] = None  # type: ignore
            else:
                obj[k] = row[v.name]
        if all(v is None for v in obj.values()):
            return None

        return cls(**obj)

    @classmethod
    def columns(cls):
        obj = dict()
        for k, v in cls.__fields__.items():
            if k in cls._excluded:
                continue
            # this field contains information that
            # is accquired with the name of the file
            if k == 'identificador_reporte':
                continue
            if issubclass(get_origin(v.outer_type_) or v.outer_type_, list):
                if issubclass(v.type_, BaseModel):
                    obj.update(v.type_.columns())
                else:
                    obj[k] = v.type_
            elif issubclass(v.type_, BaseModel):
                obj.update(v.type_.columns())
            else:
                # doing all these validations because of constrained types
                if issubclass(v.type_, str):
                    obj[k] = str
                elif issubclass(v.type_, bool):
                    obj[k] = bool
                elif issubclass(v.type_, float):
                    obj[k] = float
                elif issubclass(v.type_, int):
                    obj[k] = int
                else:
                    obj[k] = str
        return obj
