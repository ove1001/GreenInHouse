from datetime import datetime
from typing import List, Optional,Dict

from dms2223common.data.Respuesta import Respuesta
class Pregunta:

    
    
    def __init__(self, creador:str, titulo:str, descripcion:str, id:Optional[int]=None, fecha:datetime=datetime.now(),visible=True):
        self.__id:Optional[int] = id
        self.__creador:str = creador
        self.__titulo: str = titulo
        self.__descripcion: str = descripcion
        self.__fechaCreacion:datetime = fecha
        self.__visible:bool = visible
        self.__respuestas:List[Respuesta] = []
        self.__reporte = False

    def getId(self) -> Optional[int]:
        return self.__id

    def getCreador(self) -> str:
        return self.__creador

    def getTitulo(self) -> str:
        return self.__titulo

    def getDescripcion(self) -> str:
        return self.__descripcion

    def getFechaCreacion(self) -> datetime:
        return self.__fechaCreacion
    
    def getVisible(self) -> bool:
        return self.__visible

    def cambiarVisible(self):
        self.__visible = not self.__visible
    
    def getRespuestas(self) -> List[Respuesta]:
        return self.__respuestas
    
    def addRespuesta(self,respuesta:Respuesta):
        id = respuesta.getId()
        if id is not None:
            
            self.__respuestas.append(respuesta)
    
    def removeRespuesta(self,respuesta:Respuesta):
        id = respuesta.getId()
        if id is not None:
            self.__respuestas.pop(id)
    
    def getReporte(self) -> bool:
        return self.__reporte

    def reportar(self):
        self.__reporte = True

    def to_json(self,creacion=False):
        dict={}
        
        dict["creador"]=self.__creador
        dict["titulo"]=self.__titulo
        dict["descripcion"]=self.__descripcion
        dict["fecha_creacion"]=self.__fechaCreacion.isoformat()
        
        if not creacion:
            dict["id"]=self.__id
            dict["visibles"]=self.__visible
            res=[]
            for r in self.__respuestas:
                res.append(r.to_json())
            dict["respuestas"]=res
            dict["reporte"]=self.__reporte

        return dict

    def from_json(dict:Dict, creacion=False):
        if not creacion:
            pregunta = Pregunta(dict["creador"],dict["titulo"],dict["descripcion"],dict["id"])
            pregunta.__fechaCreacion=datetime.fromisoformat(dict["fecha_creacion"])
            pregunta.__visible=dict["visibles"]
            respuestas: List[Dict] = dict["respuestas"]
            for r in respuestas:
                respuesta = Respuesta.from_json(r)
                
                pregunta.addRespuesta(respuesta)
            pregunta.__reporte=dict["reporte"]
        else:
            pregunta = Pregunta(dict["creador"],dict["titulo"],dict["descripcion"],fecha=datetime.fromisoformat(dict["fecha_creacion"]))

        return pregunta