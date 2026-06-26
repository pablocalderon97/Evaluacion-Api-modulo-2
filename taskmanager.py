
import logging
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException
from modelsdb import TareaDB


DATABASE_URL = "sqlite:///./tareas.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Tarea:

    def __init__(self, titulo: str, contenido: str, creada: date, realizada: bool = False, caducada: bool = False):

        self.titulo = titulo
        self.contenido = contenido
        self.creada = creada
        self.realizada = realizada
        self.caducada = caducada

    def crear_tarea(self):     

        db = SessionLocal()

        tarea_db = TareaDB(
            titulo = self.titulo,
            contenido = self.contenido,
            creada = self.creada,
            realizada = self.realizada,
            caducada = self.caducada
         )
        
        db.add(tarea_db)
        db.commit()
        db.refresh(tarea_db)
        logging.info(f"Tarea guardada: {tarea_db.titulo}")
        db.close()
        
        return tarea_db
        

    def obtener_tarea_id(id:int):

        db = SessionLocal()
        tarea = db.query(TareaDB).filter(TareaDB.id == id).first()
        if not tarea:
            db.close()
            raise HTTPException(status_code=404, detail="Tarea no localizada")
        
        db.close()

        return{
            
            "titulo": tarea.titulo,
            "Contenido": tarea.contenido,
            "Creada": tarea.creada
        }
    
    def tarea_realizada(id:int):

        db = SessionLocal()
        tarea = db.query(TareaDB).filter(TareaDB.id == id).first()
        if not tarea:
            db.close()
            raise HTTPException(status_code=404, detail="Tarea no localizada")
        
        elif db.query(tarea.realizada) == True:
            db.close()
            raise HTTPException(status_code=400, detail="Tarea ya completada con anterioridad")

        db.query(tarea.realizada) == True

        return{
            
            "titulo": tarea.titulo,
            "Contenido": tarea.contenido,
            "Creada": tarea.creada,
            "Realizada": tarea.realizada
        }
    
    def comprobar_tareas_caducadas(fecha_actual:date):

        db = SessionLocal()
        tarea = db.query(TareaDB).filter(TareaDB.creada < fecha_actual).all()
        if not tarea:
            db.close()
            raise HTTPException(status_code=404, detail="No hay tareas caducadas")
        
        db.query(tarea.caducada) == True
        tareas_realizadas = db.query(TareaDB).filter(TareaDB.realizada == True).all()
        db.close()

        return [
         {
        "titulo": t.titulo,
        "contenido": t.contenido,
        "creada": t.creada,
        "caducada": t.caducada
         }
        
        for t in tareas_realizadas
]



        


    



