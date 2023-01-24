import hashlib
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.preguntaDB import Pregunta
from dms2223backend.data.db.exc import PreguntaExisteError
from dms2223backend.data.db.exc import PreguntaNoExisteError
from flask import current_app

class Preguntas():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, creador:str, titulo: str, descripcion: str, fecha: str) -> Pregunta:
        """ Creates a new question record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - titulo (str): The title of the question
            - descripcion (str): The description of the question

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - PreguntaExisteError: If a question with the same title already exists.

        Returns:
            - User: The created `User` result.
        """
        if not titulo or not descripcion:
            raise ValueError('A title and a description are required.')
        try:
            nueva_pregunta = Pregunta(creador,titulo, descripcion, fecha)
            session.add(nueva_pregunta)
            session.commit()
            return nueva_pregunta
        except IntegrityError as ex:
            session.rollback()
            raise PreguntaExisteError(
                'A question with title ' + titulo + ' already exists.'
                ) from ex

    @staticmethod
    def list_all(session: Session) -> List[Pregunta]:
        """Lists every user.

        Args:
            - session (Session): The session object.

        Returns:
            - List[User]: A list of `User` registers.
        """
        query = session.query(Pregunta)
        return query.all()

    @staticmethod
    def get_pregunta(session: Session, id: int) -> Optional[Pregunta]:
        """ Determines whether a user exists or not.

        Args:
            - session (Session): The session object.
            - id (str): The question id to find
            
        Returns:
            - Optional[Pregunta]: The question 
        """
        if not id:
            raise ValueError('An id is requiered.')
        try:
            query = session.query(Pregunta).filter_by(id=id)
            pregunta: Pregunta = query.one()
        except NoResultFound as ex:
            raise PreguntaNoExisteError(
                'The question with title ' + id + ' don\'t exists.'
                ) from ex
        return pregunta

    @staticmethod
    def update(session: Session,id:int):

        if not id:
            raise ValueError('An id is requiered.')
        try:
            session.query(Pregunta).filter(Pregunta.id == id).update({"visible": False})
            session.commit()
        except NoResultFound as ex:
            raise PreguntaNoExisteError(
                'The question with title ' + id + ' don\'t exists.'
                ) from ex