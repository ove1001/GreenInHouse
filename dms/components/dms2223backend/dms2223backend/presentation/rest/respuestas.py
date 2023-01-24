import traceback
from http import HTTPStatus
from flask import current_app
from dms2223backend.data.db.exc.votoexistserror import VotoExisteError
from dms2223backend.service.comentarioservice import ComentarioService
from dms2223backend.service import RespuestaService
from dms2223backend.service import PreguntaService
from dms2223common.data.Respuesta import Respuesta
from dms2223backend.service import VotoService

def get_respuestas(qid: int) :
    with current_app.app_context() :
        if PreguntaService.exists_pregunta(qid,current_app.db):
            pregunta = PreguntaService.get_pregunta(qid,current_app.db)
            respuestas = RespuestaService.list_respuestas(qid,current_app.db)
            
            for respuesta in respuestas:
                respuesta.setVotos(VotoService.count_votos_respuestas(current_app.db,respuesta.getId()))
                comentarios = ComentarioService.list_comentarios(respuesta.getId(),current_app.db)
                for comentario in comentarios:
                    comentario.setVotos(VotoService.count_votos_comentarios(current_app.db,comentario.getId()))
                    respuesta.addComentario(comentario)
                pregunta.addRespuesta(respuesta)
            return pregunta.to_json(), HTTPStatus.OK.value
        else:
            return ("La pregunta no existe", HTTPStatus.NOT_FOUND.value)

def post_respuesta(body: dict, qid: int):
    with current_app.app_context() :
        try:
            respuesta = Respuesta.from_json(body,True)
            return RespuestaService.create_respuesta_from_common(respuesta, qid ,current_app.db).to_json(), HTTPStatus.CREATED.value
        except Exception as e:
            current_app.logger.error(traceback.format_exception(e))
            return (str(e), HTTPStatus.NOT_FOUND.value)

def get_respuesta(aid : int) :
    with current_app.app_context() :
        if (RespuestaService.exists_respuesta(aid,current_app.db)) :
            return RespuestaService.get_respuesta(aid,current_app.db).to_json(),HTTPStatus.OK.value
        else :
            return ('No se ha encontrado el argumento', HTTPStatus.NOT_FOUND.value)

def post_voto(body: str, aid: int):
    with current_app.app_context() :
        try:
            VotoService.create_voto_respuesta(body.decode("utf-8"),aid,current_app.db)
            return ("",HTTPStatus.CREATED.value)
        except VotoExisteError:
            return ('El usuario ya a votado', HTTPStatus.CONFLICT.value)
        except Exception:
            return ('No existe el comentario', HTTPStatus.NOT_FOUND.value)