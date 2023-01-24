import hashlib
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.votos.votosComentarioDB import VotosComentario
from dms2223backend.data.db.exc import VotoExisteError


class VotosComentarios():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, usuario:str,id_comentario:int) -> VotosComentario:

        if not usuario or not id_comentario:
            raise ValueError('A title and a description are required.')
        try:
            nuevo_voto_comentario = VotosComentario(usuario, id_comentario)
            session.add(nuevo_voto_comentario)
            session.commit()
            return nuevo_voto_comentario
        except IntegrityError as ex:
            session.rollback()
            raise VotoExisteError(
                'A vote  with this id already exists.'
                ) from ex

    @staticmethod
    def count(session: Session,id_comentario:int) -> int:
        query = session.query(VotosComentario)
        count: List[VotosComentario] = query.filter(VotosComentario.id_comentario == id_comentario).count()
        return count