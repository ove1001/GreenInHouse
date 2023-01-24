from datetime import datetime
from typing import Dict
from sqlalchemy import Table, MetaData, Column, String , Integer, TIMESTAMP,ForeignKey,Boolean # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.resultbase import ResultBase


class VotosComentario(ResultBase):
    """ Definition and storage of comment records.
    """

    def __init__(self, usuario:str,id_comentario:int):
        """ Constructor method.
        Initializes a answer record.
        Args:
            - id_pregunta (int): A int with the question's id.
            - content (str): A string with the answer of a question
        """
        self.usuario:str = usuario
        self.id_comentario: int = id_comentario 
        
        
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
            'votosComentarios',
            metadata,
            Column('usuario',String(32), primary_key=True),          
            Column('id_comentario', Integer, ForeignKey('comentarios.id'), primary_key=True )
        )

