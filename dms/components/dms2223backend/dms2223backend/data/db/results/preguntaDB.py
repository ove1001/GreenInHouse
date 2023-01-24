import datetime 
from datetime import datetime
from typing import Dict, Optional
from sqlalchemy import Table, MetaData,ForeignKey, Column, String , Integer, TIMESTAMP, Boolean # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.resultbase import ResultBase
from dms2223backend.data.db.results.respuestaDB import Respuesta
from dms2223backend.data.db.results.reportes.reportePreguntaDB import ReportePregunta

class Pregunta(ResultBase):
    """ Definition and storage of discussion records.
    """

    def __init__(self, creador:str ,titulo:str, descripcion:str, fecha: str):
        self.id: int
        self.creador:str = creador
        self.titulo: str = titulo
        self.descripcion: str = descripcion
        self.fechaCreacion: str = fecha
        self.visible:bool = True

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.
        Args:
            - metadata (MetaData): The database schema metadata
                        (used to gather the entities' definitions and mapping)
        
        Returns:
            - Table: A `Table` object with the table definition.
        """
        return Table(
            'preguntas',
            metadata,
            Column('id', Integer, autoincrement='auto', primary_key=True),
            Column('creador',String(32),nullable=False ),
            Column('titulo', String(100), nullable=False),
            Column('descripcion', String(500), nullable=False),
            Column('fechaCreacion', String(100), nullable=False),
            Column('visible',Boolean,nullable=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ Gets the mapping properties dictionary.
        Returns:
            - Dict: A dictionary with the mapping properties.
        """
        return {
            'respuestas': relationship(Respuesta, backref='pregunta'),
            'reportepregunta': relationship(ReportePregunta, backref='reportePregunta')
        }