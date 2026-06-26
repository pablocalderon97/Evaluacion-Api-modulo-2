
import logging
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException
from main import TareaDB


DATABASE_URL = "sqlite:///./tareas.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Tarea:

    def __init__(self,id:int,titulo:str,contenido:str,creada:date,realizada:bool,caducada:bool):
        self.id = id,
        self.titulo = titulo,
        self.contenido = contenido,
        self.creada = creada,
        self.realizada = realizada,
        self.caducada = caducada

    def crear_tarea(self):

        db = SessionLocal()
        tarea_db = TareaDB(self.id,self.titulo,self.contenido,self.creada,self.realizada,self.caducada)
        
        db.add(tarea_db)
        db.commit()
        db.refresh(tarea_db)
        db.close
        
        logging.info(f"Tarea guardada correctamente en DB: {tarea_db.titulo}")

        return  {
            "msg": "tarea registrada correctamente",
            "titulo":tarea_db.titulo,
            "contenido": tarea_db.contenido,
            "creada": tarea_db.creada,
            "vencimiento": tarea_db.vencimiento,
            "realizado": tarea_db.realizada
        }        

    def obtener_tarea_id(self,id:int):

        db = SessionLocal()
        tarea = db.query(self).filter(self.id == id).first()
        if not tarea:
            db.close()
            raise HTTPException(status_code=404, detail="Tarea no localizada")
        
        db.close()

        return{
            
            "titulo": self.titulo,
            "Contenido": self.contenido,
            "Creada": self.creada
        }
    
    def tarea_realizada(self,id:int):

        db = SessionLocal()
        tarea = db.query(self).filter(self.id == id).first()
        if not tarea:
            db.close()
            raise HTTPException(status_code=404, detail="Tarea no localizada")
        
        elif db.query(self.realizada) == True:
            db.close
            raise HTTPException(status_code=400, detail="Tarea ya completada con anterioridad")

        db.query(self.realizada) == True

        return{
            
            "titulo": self.titulo,
            "Contenido": self.contenido,
            "Creada": self.creada,
            "Realizada": self.realizada
        }
    
    def comprobar_tareas_caducadas(self,fecha_actual:date):

        db = SessionLocal()
        tarea = db.query(self).filter(self.creada < fecha_actual).all()
        if not tarea:
            db.close()
            raise HTTPException(status_code=404, detail="No hay tareas caducadas")
        
        db.query(self.caducada) == True

        return{
            
            "titulo": self.titulo,
            "Contenido": self.contenido,
            "Creada": self.creada,
            "Caducada": self.caducada
        }




        


    



