import hashlib
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.respuestaDB import Respuesta
from dms2223backend.data.db.exc import RespuestaExisteError
from dms2223backend.data.db.exc import RespuestaNoExisteError


class Respuestas():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, descripcion: str, id_pregunta: int, creador:str,fecha: str) -> Respuesta:
        """ Creates a new question record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - titulo (str): The title of the question
            - descripcion (str): The description of the question

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - RespuestaExisteError: If a question with the same title already exists.

        Returns:
            - User: The created `User` result.
        """
        if not descripcion or not id_pregunta:
            raise ValueError('A title and a description are required.')
        try:
            nueva_respuesta = Respuesta(descripcion, id_pregunta, creador,fecha)
            session.add(nueva_respuesta)
            session.commit()
            return nueva_respuesta
        except IntegrityError as ex:
            session.rollback()
            raise RespuestaExisteError(
                'An answer with this id already exists.'
                ) from ex

    @staticmethod
    def list_all(session: Session,id_pregunta:int) -> List[Respuesta]:
        """Lists every user.

        Args:
            - session (Session): The session object.

        Returns:
            - List[User]: A list of `User` registers.
        """
        query = session.query(Respuesta)
        return query.where(Respuesta.id_pregunta==id_pregunta)

    @staticmethod
    def get_respuesta(session: Session, id: int) -> Optional[Respuesta]:
        """ Determines whether a user exists or not.

        Args:
            - session (Session): The session object.
            - id (str): The question id to find
            
        Returns:
            - Optional[Respuesta]: The question 
        """
        if not id:
            raise ValueError('An id is requiered.')
        try:
            query = session.query(Respuesta).filter_by(id=id)
            respuesta: Respuesta = query.one()
        except NoResultFound as ex:
            raise RespuestaNoExisteError(
                'The question with title ' + id + ' don\'t exists.'
                ) from ex
        return respuesta

    @staticmethod
    def update(session: Session,id:int):

        if not id:
            raise ValueError('An id is requiered.')
        try:
            session.query(Respuesta).filter(Respuesta.id == id).update({"visible": False})
            session.commit()
        except NoResultFound as ex:
            raise RespuestaNoExisteError(
                'The answer with title ' + id + ' don\'t exists.'
                ) from ex