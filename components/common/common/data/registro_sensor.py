from datetime import datetime
from typing import Optional,Dict,List
from enum import Enum
from common.data import TipoSensor, ZonaSensor

class RegistroSensor:

    def __init__(self, tipo_sensor:TipoSensor, zona_sensor:ZonaSensor ,numero_sensor:str, valor:float, id:int, fecha:datetime):
        self.__tipo_sensor:TipoSensor = tipo_sensor
        self.__zona_sensor:ZonaSensor = zona_sensor
        self.__numero_sensor:int = numero_sensor
        self.__valor:float = valor
        self.__id:int = id
        self.__fecha:datetime = fecha

    def getId(self) -> Optional[int]:
        return self.__id

    def getTipoSensor(self) -> TipoSensor:
        return self.__tipo_sensor
    
    def getZonaSensor(self) -> ZonaSensor:
        return self.__zona_sensor

    def getNumeroSensor(self) -> int:
        return self.__numero_sensor

    def getValor(self) -> float:
        return self.__valor

    def getFecha(self) -> datetime:
        return self.__fecha
    
    def to_json(self) -> Dict:
        dict={}
        dict["id"]=self.getId()
        dict["tipo_sensor"]=self.getTipoSensor()
        dict["zona_sensor"]=self.getZonaSensor()
        dict["numero_sensor"]=self.getNumeroSensor()
        dict["valor"]=self.getValor()
        dict["fecha"]=self.getFecha().isoformat()
        return dict

    def from_json(dict: dict):
        sensor = RegistroSensor(dict["id"],dict["tipo_sensor"],dict["zona_sensor"],dict["numero_sensor"],dict["valor"],dict["fecha"])
        return sensor
