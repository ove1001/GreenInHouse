from http import HTTPStatus
from flask import current_app
from dms2223backend.service.reporteservice import ReporteService
from dms2223backend.service.preguntaservice import PreguntaService
from dms2223backend.service.respuestaservice import RespuestaService
from dms2223backend.service.comentarioservice import ComentarioService
from dms2223common.data.Reporte import Reporte
import traceback

def post_reporte_pregunta(body: dict,qid:int):
    with current_app.app_context() :
        if PreguntaService.exists_pregunta(qid,current_app.db):
            pregunta=PreguntaService.get_pregunta(qid,current_app.db)
            return ReporteService.create_reporte_pregunta_from_common(
                Reporte.from_json(body,pregunta,True), current_app.db).to_json(), HTTPStatus.OK.value
        else:
            return ("La pregunta no existe", HTTPStatus.NOT_FOUND.value)

def get_reportes():
    with current_app.app_context() :
        reportes = ReporteService.list_reportes(current_app.db)
        salida = []
        for reporte in reportes:
            salida.append(reporte.to_json())
        return salida,HTTPStatus.OK.value
    

def set_status(body:dict):
    with current_app.app_context() :
        try:
            ReporteService.update_reporte(body["id"],body["status"],body["tipo"],current_app.db)
            return ("Reporte actualizado", HTTPStatus.ACCEPTED.NO_CONTENT.value)
        except Exception:
            return ("La pregunta no existe", HTTPStatus.NOT_FOUND.value)
    

def post_reporte_respuesta(body: dict, aid: int):
    with current_app.app_context() :
        if RespuestaService.exists_respuesta(aid,current_app.db):
            respuesta = RespuestaService.get_respuesta(aid,current_app.db)
            return ReporteService.create_reporte_respuesta_from_common(
                Reporte.from_json(body,respuesta,True), current_app.db).to_json(), HTTPStatus.OK.value
        else:
            return ("La pregunta no existe", HTTPStatus.NOT_FOUND.value)

def post_reporte_comentario(body: dict, cid: int):
    with current_app.app_context() :
        if ComentarioService.exists_comentario(cid,current_app.db):
            comentario = ComentarioService.get_comentario(cid,current_app.db)
            return ReporteService.create_reporte_comentario_from_common(
                Reporte.from_json(body,comentario,True), current_app.db).to_json(), HTTPStatus.OK.value
        else:
            return ("La pregunta no existe", HTTPStatus.NOT_FOUND.value)