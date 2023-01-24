from datetime import datetime
from typing import List
from sqlalchemy.orm.session import Session
from dms2223backend.data.db.schema import Schema  # type: ignore
from dms2223backend.data.db.results import Respuesta
from dms2223backend.data.db.resultsets import Respuestas
import dms2223common.data.Respuesta as common
from flask import current_app
class RespuestaService:

    @staticmethod
    def create_respuesta(descripcion: str, id_pregunta: int, creador:str,fecha: str, schema: Schema) -> common.Respuesta:
        session: Session = schema.new_session()
        out: common.Respuesta
        try:
            new_respuesta: Respuesta = Respuestas.create(session, descripcion, id_pregunta, creador,fecha)
            out= common.Respuesta(new_respuesta.creador,new_respuesta.descripcion,new_respuesta.id,datetime.fromisoformat(new_respuesta.fechaCreacion))
        except Exception as ex:
            current_app.logger.error(str(ex))
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def create_respuesta_from_common(respuesta: common.Respuesta, id_pregunta: int,schema: Schema) -> common.Respuesta:
        return RespuestaService.create_respuesta(respuesta.getDescripcion(), id_pregunta, respuesta.getCreador(),respuesta.getFechaCreacion().isoformat(), schema)


    @staticmethod
    def exists_respuesta(id:int, schema: Schema):
        session: Session = schema.new_session()
        respuesta = Respuestas.get_respuesta(session,id)
        respuesta_exists=True
        if respuesta is None:
            respuesta_exists=False
        schema.remove_session()
        return respuesta_exists

    @staticmethod
    def list_respuestas(id_pregunta: int, schema: Schema) -> List[common.Respuesta]:
        out: List[common.Respuesta] = []
        session: Session = schema.new_session()
        respuestas: List[Respuesta] = Respuestas.list_all(session,id_pregunta)
        for respuesta in respuestas:
            if respuesta.id_pregunta== id_pregunta:
                out.append(common.Respuesta(respuesta.creador,respuesta.descripcion,respuesta.id,datetime.fromisoformat(respuesta.fechaCreacion),respuesta.visible))
        schema.remove_session()
        return out
    
    @staticmethod
    def get_respuesta(id : int, schema: Schema) -> common.Respuesta:
        session : Session = schema.new_session()
        respuesta : Respuesta = Respuestas.get_respuesta(session, id)
        out: common.Respuesta = common.Respuesta(respuesta.creador,respuesta.descripcion,respuesta.id,datetime.fromisoformat(respuesta.fechaCreacion),respuesta.visible)
        schema.remove_session()
        return out

    @staticmethod
    def update_respuesta(id: int, schema: Schema):
        session: Session = schema.new_session()
        Respuestas.update(session,id)
        schema.remove_session()