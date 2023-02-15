from datetime import datetime
from typing import Dict, Optional
from sqlalchemy import Table, MetaData, Column, String, Enum, Integer, Float, TIMESTAMP # type: ignore
from sqlalchemy import ForeignKey  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from backend.data.db.results.modulo_base import ModuloBase
from common.data import TipoSensor, ZonaSensor

class RegistroSensor(ModuloBase):
    """ 
    Definicion y almacenamiento de los registros del sensor.
    """

    def __init__(self, tipo_sensor:TipoSensor, zona_sensor: ZonaSensor ,numero_sensor:int, valor:float, nombre_planta:str):
        self.id: int
        self.tipo_sensor: TipoSensor = tipo_sensor
        self.zona_sensor: ZonaSensor = zona_sensor
        self.numero_sensor: int = numero_sensor
        self.valor: float = valor
        self.fecha: datetime = datetime.now()
        self.nombre_planta: str = nombre_planta

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ 
        Definicion de la tabla.
        Args:
            - metadata (MetaData): Metadatos del esquema de la base de datos
                        (usado para la definicion y mapeo de entidades)
        
        Returns:
            - Table: Objeto tabla con al definicion de la tabla.
        """
        return Table(
            #str(self.tipo_sensor + str(self.numero_sensor)),
            'sensores',
            metadata,
            Column('id', Integer, autoincrement='auto', primary_key=True),
            Column('tipo_sensor',Enum(TipoSensor),nullable=False ),
            Column('zona_sensor',Enum(ZonaSensor),nullable=False ),
            Column('numero_sensor', Integer, nullable=False),
            Column('valor', Float, nullable=False),
            Column('fecha', TIMESTAMP, nullable=False),
            Column('nombre_planta', String, ForeignKey('plantas.nombre_planta'), nullable=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ 
        Obtiene el diccionario con las propiedades de mapeado.
        Returns:
            - Dict: Diccionario con las propiedades de mapeado.
        """
        return {}
