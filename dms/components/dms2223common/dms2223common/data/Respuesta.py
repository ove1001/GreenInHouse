from datetime import datetime
from typing import Optional,Dict,List
from dms2223common.data.Comentario import Comentario

class Respuesta :

    def __init__(self, creador:str, descripcion:str,id:Optional[int]=None,fecha:Optional[datetime]=datetime.now(),visible=True):
        self.__id:Optional[int] = id
        self.__creador:str = creador
        self.__fechaCreacion:datetime = fecha
        self.__descripcion:str = descripcion
        self.__visible:bool = visible
        self.__votos:int = 0
        self.__comentarios:List[Comentario] = []
        self.__votantes:List[str] =[]

    def getId(self) -> Optional[int]:
        return self.__id

    def getCreador(self) -> str:
        return self.__creador

    def getFechaCreacion(self) -> datetime:
        return self.__fechaCreacion
    
    def getDescripcion(self) -> str:
        return self.__descripcion

    # visibilidad respuesta
    def cambiarVisible(self):
        self.__visible = not self.__visible
    
    def getVisible(self) -> bool:
        return self.__visible

    def getVotos(self) -> int:
        return self.__votos
    
    def setVotos(self, votos:int):
        self.__votos=votos

    def votar(self):
        self.__votos+=1

    #crear comentario
    def addComentario(self, comentario: Comentario):
        id = comentario.getId()
        if id is not None:
            self.__comentarios.append(comentario)

    def getComentarios(self) -> list[Comentario]:
        return self.__comentarios
    
    def getVotantes(self) -> List[str]:
        return self.__votantes

    def addVotantes(self,votante:str):
        self.__votantes.append(votante)
    
    def to_json(self,creacion=False) -> Dict:
        dict={}
        dict["creador"]=self.__creador
        dict["fecha_creacion"]=self.__fechaCreacion.isoformat()
        dict["descripcion"]=self.__descripcion
        
        if not creacion:
            dict["id"]=self.__id
            dict["visible"]=self.__visible
            dict["votos"]=self.__votos
            com=[]
            for c in self.__comentarios:
                com.append(c.to_json())
            dict["comentarios"]=com
            dict["votantes"]=self.__votantes

        return dict

    def from_json(dict: dict,creacion=False):
        if not creacion:
            respuesta = Respuesta(dict["creador"],dict["descripcion"],dict["id"],datetime.fromisoformat(dict["fecha_creacion"]))
            respuesta.__visible=dict["visible"]
            respuesta.__votos=dict["votos"]
            for c in dict["comentarios"]:
                comentario = Comentario.from_json(c)
                respuesta.addComentario(comentario)
            respuesta.__votantes=dict["votantes"]
        else:
            respuesta = Respuesta(dict["creador"],dict["descripcion"],fecha=datetime.fromisoformat(dict["fecha_creacion"]))
        return respuesta