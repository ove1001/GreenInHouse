from datetime import datetime
from typing import Optional,Dict,List

class RegistroPlanta:

    def __init__(self, nombre_planta:str, tipo_planta:str, viva:bool):
        self.__nombre_planta:str = nombre_planta
        self.__tipo_planta:str = tipo_planta
        self.__viva:bool = viva

    def getNombrePlanta(self) -> str:
        return self.__nombre_planta

    def setNombrePlanta(self, nombre_planta: str):
        self.__nombre_planta = nombre_planta

    def getTipoPlanta(self) -> str:
        return self.__tipo_planta

    def setTipoPlanta(self, tipo_planta: str):
        self.__tipo_planta = tipo_planta

    def getViva(self) -> bool:
        return self.__viva

    def setViva(self, viva: bool):
        self.__viva = viva
    
    def to_json(self) -> Dict:
        dict={}
        dict["nombre_planta"]=self.__nombre_planta()
        dict["tipo_planta"]=self.__tipo_planta()
        dict["viva"]=self.__viva()
        return dict

    def from_json(dict: dict):
        sensor = RegistroPlanta(dict["nombre_planta"],dict["tipo_planta"],dict["viva"])
        return sensor
