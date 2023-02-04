from datetime import datetime
from typing import Dict, Optional
from sqlalchemy import Table, MetaData, Column, String, BigInteger, Integer, Float, TIMESTAMP # type: ignore
#from sqlalchemy import ForeignKey  # type: ignore
#from sqlalchemy.orm import relationship  # type: ignore
from backend.data.db.results.modulo_base import ModuloBase

class RegistroSensor(ModuloBase):
    """ 
    Definicion y almacenamiento de los registros del sensor.
    """

    def __init__(self, tipo_sensor:str ,numero_sensor:int, valor:float):
        self.id: int
        self.tipo_sensor: str = tipo_sensor
        self.numero_sensor: int = numero_sensor
        self.valor: float = valor
        self.fecha: datetime = datetime.now()

    @staticmethod
    def _definicion_tabla(self, metadata: MetaData) -> Table:
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
            'sensor',
            metadata,
            Column('id', BigInteger, autoincrement='auto', primary_key=True),
            Column('tipo_sensor',String(32),nullable=False ),
            Column('numero_sensor', Integer, nullable=False),
            Column('descripcion', Float, nullable=False),
            Column('fecha', TIMESTAMP, nullable=False),
        )

    @staticmethod
    def _mapeado_propiedasdes() -> Dict:
        """ 
        Obtiene el diccionario con las propiedades de mapeado.
        Returns:
            - Dict: Diccionario con las propiedades de mapeado.
        """
        return {}
