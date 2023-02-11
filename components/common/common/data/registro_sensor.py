from datetime import datetime
from typing import Optional,Dict,List

class RegistroSensor:

    def __init__(self, tipo_sensor:str ,numero_sensor:str, valor:float, id:int, fecha:datetime):
        self.__tipo_sensor:str = tipo_sensor
        self.__numero_sensor:int = numero_sensor
        self.__valor:float = valor
        self.__id:int = id
        self.__fecha:datetime = fecha

    def getId(self) -> Optional[int]:
        return self.__id

    def getTipoSensor(self) -> str:
        return self.__tipo_sensor

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
        dict["numero_sensor"]=self.getNumeroSensor()
        dict["valor"]=self.getValor()
        dict["fecha"]=self.getFecha().isoformat()
        return dict

    def from_json(dict: dict):
        sensor = RegistroSensor(dict["id"],dict["tipo_sensor"],dict["numero_sensor"],dict["valor"],dict["fecha"])
        return sensor
