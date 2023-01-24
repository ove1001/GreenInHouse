""" DiscussionEndpoints class module.
"""
from typing import List, Text, Union
from flask import redirect, request, flash, url_for, session, render_template,current_app
from werkzeug.wrappers import Response
from dms2223common.data.rest.responsedata import ResponseData
from dms2223frontend.data.rest.backendservice import BackendService
from dms2223common.data import Role
from dms2223common.data.reportstatus import ReportStatus
from dms2223frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
from dms2223common.data.Pregunta import Pregunta
from dms2223common.data.Respuesta import Respuesta
from dms2223common.data.Comentario import Comentario
from dms2223common.data.sentiment import Sentiment
from dms2223common.data.Reporte import Reporte

class DiscussionEndpoints():
    """ Monostate class responsible of handling the discussion web endpoint requests.
    """
    @staticmethod
    def get_discussion(auth_service: AuthService,backend_service: BackendService) -> Union[Response, Text]:
        """ Handles the GET requests to the discussion root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        
        response:ResponseData = backend_service.list_questions(session.get('token'))
        lista = response.get_content()
        preguntas: List[Pregunta] = []
        for p in lista:
            preguntas.append(Pregunta.from_json(p))

        return render_template('discussion.html', name=name, roles=session['roles'], preguntas=preguntas)

    @staticmethod
    def post_discussion(auth_service: AuthService,backend_service:BackendService) -> Union[Response,Text]:


        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        
        

        if request.form['titulo'] == "" or request.form['descripcion'] == "":
            flash('Introduce pregunta', 'error')
            return redirect(url_for('get_discussion'))
        
        pregunta: Pregunta = Pregunta(session['user'],request.form['titulo'],request.form['descripcion'])
        response:ResponseData = backend_service.create_question(session.get('token'),pregunta)
        pregunta = Pregunta.from_json(response.get_content())
        id = pregunta.getId()
        if id is None:
            return redirect(url_for('get_discussion'))
        
        response = backend_service.list_questions(session.get('token'))
        lista = response.get_content()
        preguntas: List[Pregunta] = []
        for p in lista:
            preguntas.append(Pregunta.from_json(p))
        return render_template('discussion.html', name=name, roles=session['roles'], preguntas=preguntas)

    
    @staticmethod
    def get_question(auth_service: AuthService,backend_service:BackendService, id_pregunta: int) -> Union[Response, Text]:
        """ Handles the GET requests to the discussion root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        name:str = session['user']
        
        
        response:ResponseData = backend_service.get_question(session.get('token'),id_pregunta)
        pregunta = Pregunta.from_json(response.get_content())

        if pregunta is None or not pregunta.getVisible():
            return redirect(url_for("get_discussion"))

        return render_template('question.html', name=name, roles=session['roles'], pregunta=pregunta)

    @staticmethod
    def post_answer(auth_service: AuthService,backend_service:BackendService,id_pregunta: int) -> Union[Response,Text]:


        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        response:ResponseData = backend_service.get_question(session.get('token'),id_pregunta)
        pregunta = Pregunta.from_json(response.get_content())
        if pregunta is None:
            return redirect(url_for("get_discussion"))

        if request.form['descripcion'] == "":
            flash('Introduce respuesta', 'error')
        else:
            respuesta = Respuesta(session["user"],request.form["descripcion"])
            backend_service.post_answer(session["token"],id_pregunta,respuesta)
        
        return redirect(url_for("get_question",id_pregunta=pregunta.getId()))


    @staticmethod
    def post_comment(auth_service: AuthService,backend_service:BackendService,id_pregunta: int,id_respuesta: int) -> Union[Response,Text]:


        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        response:ResponseData = backend_service.get_question(session.get('token'),id_pregunta)
        pregunta = Pregunta.from_json(response.get_content())

        if pregunta is None:
            return redirect(url_for("get_discussion"))

        if request.form['descripcion'] != "" and request.form['sentimiento'] != "":
            sentiment = next((x for x in Sentiment if x.value == int(request.form['sentimiento'])))
            comentario = Comentario(session['user'],request.form['descripcion'], sentiment)
            backend_service.post_comment(session["token"],id_respuesta,comentario)
        
        return redirect(url_for("get_question",id_pregunta=pregunta.getId()))

    @staticmethod
    def vote_answers(auth_service: AuthService,backend_service:BackendService,id_pregunta: int, id_respuesta: int)-> Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))


        response:ResponseData = backend_service.upvote_answer(session.get("token"),id_respuesta,session['user'])
        return redirect(url_for("get_question",id_pregunta=id_pregunta))

    @staticmethod
    def vote_comments(auth_service: AuthService,backend_service:BackendService,id_pregunta: int, id_respuesta: int, id_comentario: int)-> Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        response: ResponseData = backend_service.upvote_comments(session.get("token"),id_comentario,session['user'])
        
        return redirect(url_for("get_question",id_pregunta=id_pregunta))

    @staticmethod
    def report_answers(auth_service: AuthService, backend_service: BackendService ,id_pregunta: int, id_respuesta: int)-> Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        name:str = session['user']

        response:ResponseData = backend_service.get_question(session.get('token'),id_pregunta)
        pregunta = Pregunta.from_json(response.get_content())

        if pregunta is None:
            return redirect(url_for("get_discussion"))

        respuesta = [x for x in pregunta.getRespuestas() if x.getId() == id_respuesta][0]

        if respuesta is None:
            return redirect(url_for("get_question",id_pregunta=pregunta.getId()))
        descripcion = request.form["descripcion"]

        if descripcion is None:
            return redirect(url_for("get_discussion"))
        reporte = Reporte(descripcion,name,respuesta,ReportStatus.PENDING,0)

        response = backend_service.report_answer(session.get("token"),respuesta.getId(),reporte)
        reporte = Reporte.from_json(response.get_content(),False)
        
        return redirect(url_for("get_question",id_pregunta=pregunta.getId()))

    @staticmethod
    def report_comments(auth_service: AuthService,backend_service:BackendService,id_pregunta: int, id_respuesta: int, id_comentario: int)-> Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        name:str = session['user']

        response:ResponseData = backend_service.get_question(session.get('token'),id_pregunta)
        pregunta = Pregunta.from_json(response.get_content())

        if pregunta is None:
            return redirect(url_for("get_discussion"))

        respuesta = [x for x in pregunta.getRespuestas() if x.getId() == id_respuesta][0]

        if respuesta is None:
            return redirect(url_for("get_question",id_pregunta=pregunta.getId()))
        
        comentario= [x for x in respuesta.getComentarios() if x.getId() == id_comentario][0]
        if comentario is None:
            return redirect(url_for("get_question",id_pregunta=pregunta.getId())) 
               
        descripcion = request.form["descripcion"]

        if descripcion is None:
            return redirect(url_for("get_discussion"))
        reporte = Reporte(descripcion,name,comentario,ReportStatus.PENDING)
        response = backend_service.report_comments(session.get("token"),comentario.getId(),reporte)
        reporte = Reporte.from_json(response.get_content(),False)
        
        return redirect(url_for("get_question",id_pregunta=pregunta.getId()))

    @staticmethod
    def report_questions(auth_service: AuthService,backend_service:BackendService,id_pregunta: int)-> Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        name:str = session['user']

        response:ResponseData = backend_service.get_question(session.get('token'),id_pregunta)
        pregunta = Pregunta.from_json(response.get_content())

        if pregunta is None:
            return redirect(url_for("get_discussion"))
               
        descripcion = request.form["descripcion"]

        if descripcion is None:
            return redirect(url_for("get_discussion"))
        reporte = Reporte(descripcion,name,pregunta,ReportStatus.PENDING)

        response = backend_service.question_report(session.get("token"),pregunta.getId(),reporte)
        reporte = Reporte.from_json(response.get_content(),False)
        id = reporte.getId()

        return redirect(url_for("get_question",id_pregunta=pregunta.getId()))