from sqlalchemy.orm.session import Session
from dms2223backend.data.db.schema import Schema  # type: ignore
from dms2223backend.data.db.resultsets.votos.votosComentarioDB import VotosComentarios #voto
from dms2223backend.data.db.resultsets.votos.votosRespuestaDB import VotosRespuestas

class VotoService:

    @staticmethod
    def create_voto_respuesta(usuario:str, id_respuesta: int, schema: Schema):
        session: Session = schema.new_session()
        try:
            new_voto: VotosRespuestas = VotosRespuestas.create(session,usuario, id_respuesta)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()

    @staticmethod
    def create_voto_comentario(usuario:str, id_comentario: int, schema: Schema):
        session: Session = schema.new_session()
        try:
            new_voto: VotosComentarios = VotosComentarios.create(session,usuario,id_comentario)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()

    @staticmethod
    def count_votos_respuestas(schema: Schema,id_respuesta) -> int:
        session: Session = schema.new_session()
        out = VotosRespuestas.count(session,id_respuesta)
        schema.remove_session()
        return out

    @staticmethod
    def count_votos_comentarios(schema: Schema,id_comentario) -> int:
        session: Session = schema.new_session()
        out = VotosComentarios.count(session,id_comentario)
        schema.remove_session()
        return out