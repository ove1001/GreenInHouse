from typing import Union, List, Dict
from sqlalchemy.orm.session import Session # type: ignore
from backend.data.db.esquema import Esquema
from backend.data.db.results import RegistroPlanta
from backend.data.db.resultsets import RegistroPlantaSet
from common.data import RegistroPlanta as CommonRegistroPlanta

class RegistroPlantaService():

    @staticmethod
    # def create_registro_planta(tipo_planta: Union[TipoPlanta,str], zona_planta:Union[ZonaPlanta,str] ,numero_planta:int, valor:float, schema: Esquema) -> CommonRegistroPlanta:
    def create_registro_planta(nombre_planta: str, tipo_planta: str, schema: Esquema) -> CommonRegistroPlanta:
        session: Session = schema.new_session()
        out: CommonRegistroPlanta = None
        try:
            # if isinstance(tipo_planta, str):
            #     tipo_planta = TipoPlanta[tipo_planta]
            new_registro_planta: RegistroPlanta = RegistroPlantaSet.create(session, nombre_planta, tipo_planta)
            out= CommonRegistroPlanta(new_registro_planta.nombre_planta,new_registro_planta.tipo_planta,new_registro_planta.viva)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
    
    @staticmethod
    def create_registro_planta_from_common(registro_planta: CommonRegistroPlanta, schema: Esquema) -> CommonRegistroPlanta:
        return RegistroPlantaService.create_registro_planta(registro_planta.getTipoPlanta(), registro_planta.getNumeroPlanta(), registro_planta.getValor(), schema)

    @staticmethod
    def exists_registro_planta(nombre_planta: str, schema: Esquema):
        session: Session = schema.new_session()
        registro_planta_exists: bool = RegistroPlantaSet.get_pregunta(session, nombre_planta)
        schema.remove_session()
        return registro_planta_exists

    @staticmethod
    def list_registro_planta(schema: Esquema) -> List[CommonRegistroPlanta]:
        out: List[CommonRegistroPlanta] = []
        session: Session = schema.new_session()
        registros_planta: List[RegistroPlanta] = RegistroPlantaSet.list_all(session)
        for registro_planta in registros_planta:
            out.append(CommonRegistroPlanta(registro_planta.nombre_planta,registro_planta.tipo_planta,registro_planta.viva))
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
