from typing import List, Dict
from sqlalchemy.orm.session import Session # type: ignore
from backend.data.db.esquema import Esquema
from backend.data.db.results import RegistroSensor
from backend.data.db.resultsets import RegistroSensorSet
from common.data.registro_sensor import RegistroSensor as CommonRegistroSensor

class RegistroSensorService():

    @staticmethod
    def create_registro_sensor(tipo_sensor:str ,numero_sensor:int, valor:float, schema: Esquema) -> CommonRegistroSensor:
        session: Session = schema.new_session()
        out: CommonRegistroSensor = None
        try:
            new_registro_sensor: RegistroSensor = RegistroSensorSet.create(session, tipo_sensor, numero_sensor, valor)
            out= CommonRegistroSensor(new_registro_sensor.tipo_sensor,new_registro_sensor.numero_sensor,new_registro_sensor.valor, new_registro_sensor.id, new_registro_sensor.fecha)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
    
    @staticmethod
    def create_registro_sensor_from_common(registro_sensor: CommonRegistroSensor, schema: Esquema) -> CommonRegistroSensor:
        return RegistroSensorService.create_registro_sensor(registro_sensor.getTipoSensor(), registro_sensor.getNumeroSensor(), registro_sensor.getValor(), schema)

    @staticmethod
    def exists_registro_sensor(id:int, schema: Esquema):
        session: Session = schema.new_session()
        registro_sensor_exists: bool = RegistroSensorSet.get_pregunta(session, id)
        schema.remove_session()
        return registro_sensor_exists

    @staticmethod
    def list_registro_sensor(schema: Esquema) -> List[CommonRegistroSensor]:
        out: List[CommonRegistroSensor] = []
        session: Session = schema.new_session()
        registros_sensor: List[RegistroSensor] = RegistroSensorSet.list_all(session)
        for registro_sensor in registros_sensor:
            out.append(CommonRegistroSensor(registro_sensor.tipo_sensor,registro_sensor.numero_sensor,registro_sensor.valor, registro_sensor.id, registro_sensor.fecha))
        schema.remove_session()
        return out

'''
    @staticmethod
    def get_pregunta(id : int, schema: Schema) -> common.Pregunta:
        session : Session = schema.new_session()
        pregunta : Pregunta = Preguntas.get_pregunta(session, id)
        out= common.Pregunta(pregunta.creador,pregunta.titulo,pregunta.descripcion,pregunta.id, datetime.fromisoformat(pregunta.fechaCreacion),pregunta.visible)
        schema.remove_session()
        return out

    @staticmethod
    def update_pregunta(id:int,schema: Schema):
        session: Session = schema.new_session()
        Preguntas.update(session,id)
        schema.remove_session()
'''
