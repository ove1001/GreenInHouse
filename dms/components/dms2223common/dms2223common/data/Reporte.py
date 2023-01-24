from datetime import datetime
from typing import Optional
from dms2223common.data.reportstatus import ReportStatus
from dms2223common.data.Comentario import Comentario
from dms2223common.data.Pregunta import Pregunta
from dms2223common.data.Respuesta import Respuesta
from flask import current_app

class Reporte:


    def __init__(self, descripcion:str, autor:str, elemento:Pregunta|Respuesta|Comentario, estado:ReportStatus, id:Optional[int]= None,fecha: datetime=datetime.now()):
        self.__id:Optional[int] = id
        self.__descripcion: str = descripcion
        self.__autor:str = autor
        self.__fechaReporte:datetime = fecha
        self.__elemento: Pregunta|Respuesta|Comentario  = elemento
        self.__estado: ReportStatus = estado
        if ( isinstance(elemento,Pregunta) ):
            self.__tipoElemento = "pregunta"
        elif ( isinstance(elemento,Respuesta) ):
            self.__tipoElemento = "respuesta"
        elif ( isinstance(elemento,Comentario) ):
            self.__tipoElemento = "comentario"

    def getId(self) -> Optional[int]:
        return self.__id

    def getDescripcion(self) -> str:
        return self.__descripcion
    
    def getAutor(self) -> str:
        return self.__autor
    
    def getFechaReporte(self) -> datetime:
        return self.__fechaReporte
    
    def getElemento(self):
        return self.__elemento

    def setEstado(self,estado):
        self.__estado=estado
    
    def getEstado(self) -> ReportStatus:
        return self.__estado

    def getTipoElemento(self) -> str:
        return self.__tipoElemento

    def to_json(self,creacion = False) -> dict:
        json = {}
        json["autor"] = self.__autor
        json["descripcion"] = self.__descripcion
        json["elemento"] = self.__elemento.getId()
        json["fechaReporte"] = self.__fechaReporte.isoformat()
        json["estado"] = self.__estado.name
        json["tipo"] = self.__tipoElemento
        if not creacion:
            json["id"] = self.__id
        return json

    def from_json(json: dict,elemento: Pregunta|Respuesta|Comentario,creacion: bool=False):
        estado = next((x for x in ReportStatus if x.name == json["estado"]))
        if not creacion:
            r=Reporte(json["descripcion"],json["autor"],elemento,estado,json["id"],datetime.fromisoformat(json["fechaReporte"]))
        else:
            r=Reporte(json["descripcion"],json["autor"],elemento,estado,datetime.fromisoformat(json["fechaReporte"]))
        return r