import hashlib
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.results.votos.votosRespuestaDB import VotosRespuesta
from dms2223backend.data.db.exc import VotoExisteError
class VotosRespuestas():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, usuario:str,id_respuesta:int) -> VotosRespuesta:
        """ Creates a new question record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - titulo (str): The title of the question
            - descripcion (str): The description of the question

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - VotoExisteError: If a question with the same title already exists.

        Returns:
            - User: The created `User` result.
        """
        if not usuario or not id_respuesta:
            raise ValueError('A title and a description are required.')
        try:
            nuevo_voto_respuesta = VotosRespuesta(usuario, id_respuesta)
            session.add(nuevo_voto_respuesta)
            session.commit()
            return nuevo_voto_respuesta
        except IntegrityError as ex:
            session.rollback()
            raise VotoExisteError(
                'A vote  with this id already exists.'
                ) from ex

    @staticmethod
    def count(session: Session,id_respuesta:int) -> int:
        """Lists every user.

        Args:
            - session (Session): The session object.

        Returns:
            - List[User]: A list of `User` registers.
        """
        query = session.query(VotosRespuesta)
        count: List[VotosRespuesta] = query.filter(VotosRespuesta.id_respuesta == id_respuesta).count()
        return count