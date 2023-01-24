from http import HTTPStatus
from flask import current_app
from dms2223backend.service import PreguntaService
import dms2223common.data.Pregunta as common

def get_preguntas() :
    with current_app.app_context() :
        preguntas: list[common.Pregunta] = PreguntaService.list_preguntas(current_app.db)
        salida = []
        for pregunta in preguntas:
            salida.append(pregunta.to_json())
            
        return salida, HTTPStatus.OK.value

def post_pregunta(body: dict):
    with current_app.app_context() :
        try:
            
            pregunta=common.Pregunta.from_json(body,True)
            return PreguntaService.create_pregunta_from_common(pregunta, current_app.db).to_json(), HTTPStatus.CREATED.value
        except Exception:
            return ('No se ha creado el argumento', HTTPStatus.NOT_FOUND.value)

def get_pregunta(qid: int):
    with current_app.app_context() :
        if (PreguntaService.exists_pregunta(qid,current_app.db)) :
            return PreguntaService.get_pregunta(qid,current_app.db), HTTPStatus.NOT_FOUND.value
        else:
            return ('No se ha encontrado el argumento', HTTPStatus.NOT_FOUND.value)

