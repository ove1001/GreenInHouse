""" 
Modulo de clase Esquema
"""

from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker, scoped_session, registry  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from data.config import BackendConfiguration
from compenents.backend.backend.data.db.results.registro_sensor import Sensor


# Required for SQLite to enforce FK integrity when supported
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(
    dbapi_connection, connection_record):  # pylint: disable=unused-argument
    """ Sets the SQLite foreign keys enforcement pragma on connection.
    Args:
        - dbapi_connection: The connection to the database API.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.close()

class Esquema:
    """ Class responsible of the schema initialization and session generation.
    """
    def __init__(self, config: BackendConfiguration):
        """ Constructor method.
        Initializes the schema, deploying it if necessary.
        Args:
            - config (AuthConfiguration): The instance with the schema connection parameters.
        Raises:
            - RuntimeError: When the connection cannot be created/established.
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
        Sensor.map(self.__registry)

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