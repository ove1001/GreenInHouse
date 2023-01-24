from datetime import datetime
from typing import List, Dict
from sqlalchemy.orm.session import Session
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results import Pregunta
from dms2223backend.data.db.resultsets import Preguntas
import dms2223common.data.Pregunta as common
class PreguntaService():

    @staticmethod
    def create_pregunta(titulo: str, descripcion: str, creador:str, fecha: str, schema: Schema) -> common.Pregunta:
        session: Session = schema.new_session()
        out: common.Pregunta = None
        try:
            new_pregunta: Pregunta = Preguntas.create(session, creador, titulo, descripcion, fecha)
            out= common.Pregunta(new_pregunta.creador,new_pregunta.titulo,new_pregunta.descripcion,new_pregunta.id, datetime.fromisoformat(new_pregunta.fechaCreacion))
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
    
    @staticmethod
    def create_pregunta_from_common(pregunta: common.Pregunta, schema: Schema) -> common.Pregunta:
        return PreguntaService.create_pregunta(pregunta.getTitulo(), pregunta.getDescripcion(), pregunta.getCreador(), pregunta.getFechaCreacion(), schema)

    @staticmethod
    def exists_pregunta(id:int, schema: Schema):
        session: Session = schema.new_session()
        pregunta_exists: bool = Preguntas.get_pregunta(session, id)
        schema.remove_session()
        return pregunta_exists

    @staticmethod
    def list_preguntas(schema: Schema) -> List[common.Pregunta]:
        out: List[common.Pregunta] = []
        session: Session = schema.new_session()
        preguntas: List[Pregunta] = Preguntas.list_all(session)
        for pregunta in preguntas:
            out.append(common.Pregunta(pregunta.creador,pregunta.titulo,pregunta.descripcion,pregunta.id, datetime.fromisoformat(pregunta.fechaCreacion),pregunta.visible))
        schema.remove_session()
        return out

    @staticmethod
    def get_pregunta(id : int, schema: Schema) -> common.Pregunta:
        session : Session = schema.new_session()
        pregunta : Pregunta = Preguntas.get_pregunta(session, id)
        out= common.Pregunta(pregunta.creador,pregunta.titulo,pregunta.descripcion,pregunta.id, datetime.fromisoformat(pregunta.fechaCreacion),pregunta.visible)
        schema.remove_session()
        return out

    @staticmethod
    def update_pregunta(id:int,schema: Schema):
        session: Session = schema.new_session()
        Preguntas.update(session,id)
        schema.remove_session()
