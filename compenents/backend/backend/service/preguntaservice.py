from datetime import datetime
from typing import List, Dict
from sqlalchemy.orm.session import Session # type: ignore
from backend.data.db.esquema import Esquema
from backend.data.db.results import Sensor
from backend.data.db.resultsets import SensorSet
import common.data.registro_sensor as RegistroSensor

class RegistroSensorService():

    @staticmethod
    def create_registro_sensor(tipo_sensor:str ,numero_sensor:int, valor:float, schema: Esquema) -> RegistroSensor:
        session: Session = schema.new_session()
        out: RegistroSensor = None
        try:
            new_registro_sensor: Sensor = SensorSet.create(session, tipo_sensor, numero_sensor, valor)
            out= RegistroSensor(new_registro_sensor.tipo_sensor,new_registro_sensor.numero_sensor,new_registro_sensor.valor, new_registro_sensor.id, new_registro_sensor.fecha)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
    
    @staticmethod
    def create_registro_sensor_from_common(pregunta: common.Pregunta, schema: Esquema) -> common.Pregunta:
        return PreguntaService.create_pregunta(pregunta.getTitulo(), pregunta.getDescripcion(), pregunta.getCreador(), pregunta.getFechaCreacion(), schema)

    @staticmethod
    def exists_registro_sensor(id:int, schema: Esquema):
        session: Session = schema.new_session()
        pregunta_exists: bool = Preguntas.get_pregunta(session, id)
        schema.remove_session()
        return pregunta_exists

    @staticmethod
    def list_registro_sensor(schema: Esquema) -> List[common.Pregunta]:
        out: List[common.Pregunta] = []
        session: Session = schema.new_session()
        preguntas: List[Pregunta] = Preguntas.list_all(session)
        for pregunta in preguntas:
            out.append(common.Pregunta(pregunta.creador,pregunta.titulo,pregunta.descripcion,pregunta.id, datetime.fromisoformat(pregunta.fechaCreacion),pregunta.visible))
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
