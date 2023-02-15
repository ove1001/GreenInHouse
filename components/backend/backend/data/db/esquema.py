""" 
Modulo de clase Esquema
"""

from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker, scoped_session, registry  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from backend.data.config import BackendConfiguration
from backend.data.db.results import RegistroSensor, RegistroPlanta


# Requerido por SQLite para forzxar la integridad de claves foraneas
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(
    conexion_dbapi, connection_record):  # pylint: disable=unused-argument
    """ 
    Activacion de las claves foraneas de SQLite al realizar la conexion a la base de datos
    Args:
        - dbapi_connection: Conexion de API a la base de datos
    """
    cursor = conexion_dbapi.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.close()

class Esquema:
    """ Class responsible of the schema initialization and session generation.
    """
    def __init__(self, config: BackendConfiguration):
        """ 
        Inicializacion del esquema de la base de datos
        Args:
            - config (AuthConfiguration): Instancia con los parametros de conexion del esquema.
        Raises:
            - RuntimeError: Cuando la conexion no se puede crear o establecer.
        """
        self.__registry = registry()
        if config.get_db_connection_string() is None:
            raise RuntimeError(
                'Es necesario establecer un valor en la configuracion del parametro `db_connection_string`'
            )
        db_connection_string: str = config.get_db_connection_string() or ''
        self.__create_engine = create_engine(db_connection_string)
        self.__session_maker = scoped_session(sessionmaker(bind=self.__create_engine))

        #TODO
        RegistroPlanta.map(self.__registry)
        RegistroSensor.map(self.__registry)

        self.__registry.metadata.create_all(self.__create_engine)

        
    def new_session(self) -> Session:
        """ 
        Construccion de una nueva sesion
        Returns:
            - Session: Un nuevo objeto de Session.
        """
        return self.__session_maker()

    def remove_session(self) -> None:
        """
        Liberar el recurso existente de hilo de sesion
        """
        self.__session_maker.remove()