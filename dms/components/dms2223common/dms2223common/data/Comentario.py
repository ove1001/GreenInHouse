from datetime import datetime
import json
from typing import Dict, Optional,List
from flask import current_app
from dms2223common.data.sentiment import Sentiment
class Comentario:

    

    def __init__(self, creador:str, descripcion:str, sentimiento: Sentiment,id:Optional[int] = None,fecha:datetime=datetime.now(),visible=True):
        self.__id:Optional[int] = id
        self.__creador:str = creador
        self.__descripcion: str= descripcion
        self.__fechaCreacion:datetime = fecha
        self.__visible:bool= visible
        self.__votos:int= 0
        self.__sentimiento: Sentiment =sentimiento
        self.__votantes:List[str] =[]

    def getId(self) -> Optional[int]:
        return self.__id

    def getCreador(self) -> str:
        return self.__creador

    def getDescripcion(self) -> str:
        return self.__descripcion

    def getFechaCreacion(self) -> datetime:
        return self.__fechaCreacion

    def cambiarVisible(self):
        self.__visible = not self.__visible
    
    def getVisible(self) -> bool:
        return self.__visible

    def setVotos(self,votos:int):
        self.__votos = votos
    
    def getVotos(self) -> int:
        return self.__votos 

    def getSentimiento(self) -> Sentiment:
        return self.__sentimiento

    def setSentimiento(self,sentimiento):
        self.__sentimiento=sentimiento

    def getVotantes(self) -> List[str]:
        return self.__votantes

    def addVotantes(self,votante):
        self.__votantes.append(votante)

    def to_json(self,creacion=False) -> Dict:
        dict = {}
        
        dict["creador"]=self.__creador
        dict["descripcion"]=self.__descripcion
        dict["sentimiento"]=self.__sentimiento.name
        dict["fecha_creacion"]=self.__fechaCreacion.isoformat()
        if not creacion:
            dict["id"]=self.__id
            dict["visible"]=self.__visible
            dict["votos"]=self.__votos
            dict["votantes"]=self.__votantes
        return dict

    def from_json(dict,creacion=False):
        if not creacion:
            sentiment = next(x for x in Sentiment if x.name == dict["sentimiento"])
            comentario = Comentario(dict["creador"],dict["descripcion"],sentiment ,dict["id"],datetime.fromisoformat(dict["fecha_creacion"]))
            comentario.__visible=dict["visible"]
            comentario.__votos=dict["votos"]
            comentario.__votantes=dict["votantes"]
        else:
            sentiment = next(x for x in Sentiment if x.name == dict["sentimiento"])
            
            comentario = Comentario(dict["creador"],dict["descripcion"],sentiment,fecha=datetime.fromisoformat(dict["fecha_creacion"]))
        return comentario