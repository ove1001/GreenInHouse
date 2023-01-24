from datetime import datetime
from typing import List
from sqlalchemy.orm.session import Session
from dms2223backend.data.db.schema import Schema  # type: ignore
from dms2223backend.data.db.results import Comentario
from dms2223backend.data.db.resultsets import Comentarios
from dms2223backend.data.db.results.votos import VotosComentario
import dms2223common.data.Comentario as common
from dms2223common.data.sentiment import Sentiment

class ComentarioService:

    @staticmethod
    def create_comentario(descripcion: str, id_respuesta: int, creador:str, sentimiento: Sentiment,fecha: str, schema: Schema) -> common.Comentario:
        session: Session = schema.new_session()
        out: common.Comentario = None
        try:
            new_comentario: Comentario = Comentarios.create(session, descripcion, id_respuesta, creador, sentimiento,fecha)
            out = common.Comentario(new_comentario.creador,new_comentario.descripcion,new_comentario.sentimiento,new_comentario.id,datetime.fromisoformat(new_comentario.fechaCreacion))
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def create_comentario_from_common(comentario: common.Comentario, id_respuesta: int, schema: Schema) -> common.Comentario:
        return ComentarioService.create_comentario(comentario.getDescripcion(), id_respuesta, comentario.getCreador(), comentario.getSentimiento(), comentario.getFechaCreacion().isoformat(), schema)

    @staticmethod
    def exists_comentario(id:int, schema: Schema) -> bool:
        session: Session = schema.new_session()
        comentario_exists: bool = Comentarios.get_comentario(session,id)
        schema.remove_session()
        return comentario_exists

    @staticmethod
    def list_comentarios(id_respuesta: int, schema: Schema) -> List[common.Comentario]:
        out: List[common.Comentario] = []
        session: Session = schema.new_session()
        comentarios: List[Comentario] = Comentarios.list_all(session,id_respuesta)
        for comentario in comentarios:
            if comentario.id_respuesta== id_respuesta:
                out.append(common.Comentario(comentario.creador,comentario.descripcion,comentario.sentimiento,comentario.id,datetime.fromisoformat(comentario.fechaCreacion),comentario.visible))
        schema.remove_session()
        return out

    @staticmethod
    def get_comentario(id : int, schema: Schema) -> common.Comentario:
        session : Session = schema.new_session()
        comentario : Comentario = Comentarios.get_comentario(session, id)
        out: common.Comentario = common.Comentario(comentario.creador,comentario.descripcion,comentario.sentimiento,comentario.id,datetime.fromisoformat(comentario.fechaCreacion),comentario.visible)
        schema.remove_session()
        return out

    @staticmethod
    def update_comentario(id:int,schema: Schema):
        session: Session = schema.new_session()
        Comentarios.update(session,id)
        schema.remove_session()