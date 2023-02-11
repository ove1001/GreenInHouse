#import hashlib
#from flask import current_app

from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from backend.data.db.results.registro_sensor import RegistroSensor
from backend.data.db.exc.error_sensor_existe import ErrorSensorExiste
from backend.data.db.exc.error_sensor_no_existe import ErrorSensorNoExiste
from backend.data.db.exc.error_registro_sensor_existe import ErrorRegistroSensorExiste
from backend.data.db.exc.error_registro_sensor_no_existe import ErrorRegistroSensorNoExiste

class RegistroSensorSet():
    """ 
    Clase responsable a nivel de tabla de las operaciones con los registros.
    """
    @staticmethod
    def create(session: Session, tipo_sensor:str ,numero_sensor:int, valor:float) -> RegistroSensor:
        """
        Creacion de un nuevo registro de un sensor

        Nota:
            Realiza commit de la transaccion.

        Args:
            - session (Session): Objeto de sesion.
            - tipo_sensor (str): Tipo de sensor.
            - numero_sensor (str): Numero de sensor.
            - valor (float): Valor de lectura del sensor.

        Raises:
            - ValueError: Si no es proporcionado alguno de los datos necesarios.
            - ErrorRegistroSensorExiste: Si el registro del sensor ya existe.

        Returns:
            - Sensor: Registro creado del sensor.
        """
        if not tipo_sensor:
            raise ValueError('Necesario especificar el tipo de sensor.')
        if not numero_sensor:
            raise ValueError('Necesario especificar el numero de sensor.')
        if not valor:
            raise ValueError('Necesario especificar el valor del sensor.')
        try:
            nuevo_registro = RegistroSensor(tipo_sensor,numero_sensor, valor)
            session.add(nuevo_registro)
            session.commit()
            return nuevo_registro
        except IntegrityError as ex:
            session.rollback()
            raise ErrorRegistroSensorExiste(
                'El registro ' + str(nuevo_registro.id) + ' del sensor ' + str(nuevo_registro.numero_sensor) + ' de ' +  nuevo_registro.tipo_sensor + 'ya existe.'
                ) from ex

    @staticmethod
    def list_all(session: Session) -> List[RegistroSensor]:
    #def list_all(session: Session, tipo_sensor:str ,numero_sensor:str) -> List[Sensor]:
        """Lists every user.

        Args:
            - session (Session): Objeto de sesion.

        Returns:
            - List[User]: Lista de registros del sensor.
        """
        query = session.query(RegistroSensor)
        return query.all()

'''
    @staticmethod
    def get_pregunta(session: Session, id: int) -> Optional[Sensor]:
        """ Determines whether a user exists or not.

        Args:
            - session (Session): Objeto de sesion.
            - id (str): The question id to find
            
        Returns:
            - Optional[Pregunta]: The question 
        """
        if not id:
            raise ValueError('An id is requiered.')
        try:
            query = session.query(Sensor).filter_by(id=id)
            sensor: Sensor = query.one()
        except NoResultFound as ex:
            raise ErrorRegistroSensorNoExiste(
                'The question with title ' + id + ' don\'t exists.'
                ) from ex
        return sensor

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
'''