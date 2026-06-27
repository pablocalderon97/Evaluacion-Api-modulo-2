
import logging
from datetime import datetime, date
from fastapi import FastAPI, HTTPException
from modelsdb import TareaDB

class Tarea:

    
    _dict_tareas = {}
    _contador_id = 0


    def __init__(self, titulo: str, contenido: str, creada: date, deadline: date, realizada: bool = False, caducada: bool = False):

        Tarea._contador_id += 1
        self.__id = Tarea._contador_id
        self.__titulo = titulo
        self.__contenido = contenido
        self.__creada = creada
        self.__deadline = deadline
        self.__realizada = realizada
        self.__caducada = caducada

        Tarea._dict_tareas[self.__id] = self

    def valores_tareas(self):
          return{
            
            "id": self.__id,
            "titulo": self.__titulo,
            "contenido": self.__contenido,
            "creada": self.__creada,
            "deadline": self.__deadline,
            "realizada": self.__realizada,
            "caducada": self.__caducada
         }
    
    def get_id(self): 
        return self.__id
    
    def get_titulo(self):
        return self.__titulo
    
    def set_titulo(self, valor: str): 
        self.__titulo = valor
        
    def get_contenido(self):
        return self.__contenido
    
    def set_contenido(self, valor: str): 
        self.__contenido = valor

    def get_creada(self):
        return self.__creada
    
    def set_creada(self, valor: date): 
        self.__creada = valor
    
    def get_deadline(self):
        return self.__deadline
    
    def set_deadline(self, valor: date): 
        self.__deadline = valor        
    
    def get_realizada(self): 
        return self.__realizada
    
    def set_realizada(self, valor: bool): 
        self.__realizada = valor

    def get_caducada(self): 
        return self.__caducada

    def set_caducada(self, valor: bool): 
        self.__caducada = valor

    @classmethod
    def crear_tarea(cls, titulo:str,contenido:str,creada:date,deadline:date,realizada:bool = False, caducada:bool = False): 

        tarea = cls(titulo,contenido,creada,deadline,realizada,caducada)
        return tarea.valores_tareas()

    @classmethod
    def listar_tareas(cls):

        if not cls._dict_tareas:
            raise HTTPException(status_code=404, detail="No hay tareas")
        
        return [t.valores_tareas() for t in cls._dict_tareas.values()]
  

    @classmethod
    def obtener_por_id(cls, id: int):

        tarea = cls._dict_tareas.get(id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return tarea.valores_tareas()
    
    @classmethod
    def tarea_realizada(cls, id: int):

        tarea = cls._dict_tareas.get(id)

        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        if tarea.get_realizada():
            raise HTTPException(status_code=400, detail="La tarea ya estaba completada")
        
        tarea.set_realizada(True)

        return tarea.valores_tareas()
    
    @classmethod
    def comprobar_caducadas(cls, fecha_actual: date):
    
        caducadas = []

        for t in cls._dict_tareas.values():
               
            if t.get_deadline() and t.get_deadline() < fecha_actual and not t.get_caducada():

                t.set_caducada(True)  
                caducadas.append(t)    

        if not caducadas:
            raise HTTPException(status_code=404, detail="No hay tareas caducadas")

        return [t.valores_tareas() for t in caducadas] 
        
    



