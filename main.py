import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator,model_validator
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Tarea(BaseModel):
    titulo: str = Field(..., min_length=5, description="Titulo de la tarea a realizar (minimo 5 caracteres)")
    contenido: str = Field(..., description="Contenido de la tarea a realizar")
    creada: datetime.now = Field(...,ge=0,description="Hora de la creacion de la tarea")
    vencimiento: int = Field(..., ge=0, description="Hora a la que caduca la tarea a realizar")
    realizada: bool = Field(False,description="Estado de la tarea") # Lo inicializo a falso siempre para luego poder cambiarlo en BD con PUT una vez completada la tarea
    caducada: bool = Field(False,description="Estado si la tarea a caducado o no")

    
app = FastAPI(
    title="Evaluacion modulo programacion avanzada, api con tareas a realizar"
    description="API de ejemplo con base de datos SQLite."
    version="1.0.0"
)

@app.post("/task/")
def crear_tarea(tarea:Tarea):
    logging.info(f"Tarea procesada correctamente: {tarea}")

    db = SessionLocal()
    
    tarea_bd = Tarea(titulo=tarea.titulo,contenido=tarea.contenido,creada=tarea.creada,vencimiento=tarea.vencimiento,realizada=tarea.realizada,caducada=tarea.caducada)
    db.add(tarea_bd)
    db.commit()
    db.refresh(tarea_bd)
    db.close
    logging.info(f"Tarea guardada correctamente en DB: {tarea_bd.titulo}")

    return{
        "msg": "tarea registrada correctamente",
        "tarea":{
            "titulo": tarea_bd.titulo,
            "contenido": tarea_bd.contenido,
            "creada": tarea_bd.creada,
            "vencimiento": tarea_bd.vencimiento,
            "realizado": tarea_bd.realizada
            a:a

        }
    
    }