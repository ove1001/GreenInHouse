""" ModeratorEndpoints class module.
"""

from typing import Dict, Text, Union
from flask import redirect, url_for, session, render_template, request, current_app
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223common.data.Comentario import Comentario
from dms2223common.data.Pregunta import Pregunta
from dms2223common.data.Respuesta import Respuesta
from dms2223frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
from dms2223common.data.reportstatus import ReportStatus
from dms2223common.data.Reporte import Reporte
from dms2223frontend.data.rest.backendservice import BackendService
reportes: list[Reporte] = []
class ModeratorEndpoints():
    """ Monostate class responsible of handing the moderator web endpoint requests.
    """
    @staticmethod
    def get_moderator(auth_service: AuthService,backend_service: BackendService) -> Union[Response, Text]:
        """ Handles the GET requests to the moderator root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name:str = session['user']
        response = backend_service.list_reports(session.get("token"))
        lista = response.get_content()
        reportes.clear()
        #reportes: list[Reporte] = []
        for i in lista:
            if i["tipo"] == "pregunta":
                response = backend_service.get_question(session.get("token"),i["elemento"])
                elemento = Pregunta.from_json(response.get_content())
            elif i["tipo"] == "respuesta":
                response = backend_service.get_answer(session.get("token"),i["elemento"])
                elemento = Respuesta.from_json(response.get_content())
            else:
                response = backend_service.get_comment(session.get("token"),i["elemento"])
                elemento = Comentario.from_json(response.get_content())
            reportes.append(Reporte.from_json(i,elemento,False))
        current_app.logger.debug(reportes)
        return render_template('moderator.html', name=name, roles=session['roles'],reportes=reportes)

    @staticmethod
    def post_report(auth_service: AuthService,backend_service: BackendService,id_reporte: int):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        
        reporte = [x for x in reportes if x.getId() == id_reporte][0]

        if reporte is None:
            return redirect(url_for("get_moderator"))
        
        if request.form["opcion"] == "aceptar":
            if reporte.getElemento() is not None:
                reporte.getElemento().cambiarVisible()
            reporte.setEstado(ReportStatus.ACCEPTED)
        elif request.form["opcion"] == "rechazar":
            reporte.setEstado(ReportStatus.REJECTED)
        backend_service.change_report(session.get("token"),reporte)
        return redirect(url_for("get_moderator"))