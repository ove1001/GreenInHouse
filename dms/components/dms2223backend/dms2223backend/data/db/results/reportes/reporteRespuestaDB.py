from datetime import datetime
from typing import Dict
from sqlalchemy import Table, MetaData, Column, String , Integer, TIMESTAMP,Enum,ForeignKey,Boolean # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.resultbase import ResultBase
from dms2223common.data import Comentario, Pregunta, Respuesta
from dms2223common.data.reportstatus import ReportStatus


class ReporteRespuesta(ResultBase):
    """ Definition and storage of comment records.
    """

    def __init__(self,descripcion:str, creador:str, estado:ReportStatus,id_respuesta : int,fecha:str):
        """ Constructor method.
        Initializes a answer record.
        Args:
            - id_respuesta (int): A int with the question's id.
        """
        self.id:int
        self.id_respuesta : int = id_respuesta
        self.descripcion: str = descripcion
        self.creador:str = creador
        self.fechaCreacion:str = fecha
        self.estado: ReportStatus = estado
        self.tipoElemento = "respuesta"
        
        
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
            'reporteRespuestas',
            metadata,
            Column('id', Integer, autoincrement='auto', primary_key=True), 
            Column('creador',String(32),nullable=False ),          
            Column('descripcion', String(500), nullable=False),
            Column('id_respuesta', Integer, ForeignKey('respuestas.id'), nullable=False),
            Column('fechaCreacion', String(100), nullable=False),
            Column('estado',Enum(ReportStatus),default= ReportStatus.PENDING.name,nullable=False) 
            
        )
    # @staticmethod
    # def _mapping_properties() -> Dict:
    #     # Definimos la "relación" entre comentarios y votos
    #     return {
    #         'votos': relationship(Votos, backref='id'),
    #         'reportes': relationship(Reporte, backref='id') #añadir votos y backref
    #     }

