from datetime import datetime
from typing import Dict, Optional
from sqlalchemy import Table, MetaData, Column, String, Boolean # type: ignore
from sqlalchemy import ForeignKey  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from backend.data.db.results import ModuloBase, RegistroSensor

class RegistroPlanta(ModuloBase):
    """ 
    Definicion y almacenamiento de los registros del sensor.
    """

    def __init__(self, nombre_planta:str, tipo_planta:str):
        self.nombre_planta: str = nombre_planta
        self.tipo_planta: str = tipo_planta
        self.viva: bool = True

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
            'plantas',
            metadata,
            Column('nombre_planta', String, primary_key=True),
            Column('tipo_planta', String, nullable=False ),
            Column('viva', Boolean, nullable=False ),
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ 
        Obtiene el diccionario con las propiedades de mapeado.
        Returns:
            - Dict: Diccionario con las propiedades de mapeado.
        """
        return {
            #'registro_sensores': relationship(RegistroSensor, backref='nombre_planta')
        }
