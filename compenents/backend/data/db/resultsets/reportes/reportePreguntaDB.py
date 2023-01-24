import hashlib
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.reportes.reportePreguntaDB import ReportePregunta
from dms2223backend.data.db.exc import ReporteNoExisteError
from dms2223backend.data.db.exc import ReporteExisteError
from dms2223common.data.reportstatus import ReportStatus

class ReportePreguntas():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, descripcion:str, creador:str,id_pregunta : int, estado: ReportStatus,fecha: str) -> ReportePregunta:
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
            nuevo_reporte = ReportePregunta(descripcion, creador, estado, id_pregunta,fecha)
            session.add(nuevo_reporte)
            session.commit()
            return nuevo_reporte
        except IntegrityError as ex:
            session.rollback()
            raise ReporteExisteError(
                'An report with this id already exists.'
                ) from ex

    @staticmethod
    def list_all(session: Session) -> List[ReportePregunta]:
        """Lists every user.

        Args:
            - session (Session): The session object.

        Returns:
            - List[User]: A list of `User` registers.
        """
        query = session.query(ReportePregunta)
        return query.where(ReportePregunta.estado=="PENDING")

    @staticmethod
    def get_reporte(session: Session, id: int) -> Optional[ReportePregunta]:
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
            query = session.query(ReportePregunta).filter_by(id=id)
            reporte: ReportePregunta = query.one()
        except NoResultFound as ex:
            raise ReporteNoExisteError(
                'The report with id ' + id + ' don\'t exists.'
                ) from ex
        return reporte

    @staticmethod
    def update_reporte(session:Session,id:int,estado):


        if not id:
            raise ValueError("An id is requiered.")
        try:
            query = session.query(ReportePregunta).filter(ReportePregunta.id == id)
            query.update({"estado": estado})
            session.commit()
        except NoResultFound as ex:
            raise ReporteNoExisteError(
                f"The report with id {id} doesn't exists."
            ) from ex