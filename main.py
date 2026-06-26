import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator,model_validator
from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from modelsdb import Base, TareaDB, CrearTarea , engine
from taskmanager import Tarea

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

class CrearTarea(BaseModel):
    id: Optional[int] = None
    titulo: str = Field(..., min_length=5, description="Titulo de la tarea a realizar (minimo 5 caracteres)")
    contenido: str = Field(..., description="Contenido de la tarea a realizar")
    creada: date = Field(...,description="Fecha de la creacion de la tarea")
    realizada: Optional[bool] = Field(default=False,description="Estado de la tarea") # Lo inicializo a falso para luego poder cambiarlo en BD con PUT una vez completada la tarea
    caducada: Optional[bool] = Field(default=False,description="Estado si la tarea a caducado o no") # Lo inicializo a falso para luego comprobarlo con GET
    
# Creacion API

app = FastAPI(
    title="Evaluacion modulo programacion avanzada, api con tareas a realizar",
    description="API de ejemplo con base de datos SQLite.",
    version="1.0.0"
)

# EndPoints

@app.get("/tasks/{id}")
def listar_tareas(id:int):

    Tarea.obtener_tarea_id(id)
    
@app.get("/tasks/caducadas")
def tareas_caducadas(fecha:date):

    fecha = date.today()
    Tarea.comprobar_tareas_caducadas(fecha)

@app.put("/tasks/{id}/completada")
def completar_tarea(tarea:CrearTarea,id:int):

    Tarea.tarea_realizada(tarea,id)

@app.post("/tasks/",status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea:CrearTarea):
    
    logging.info(f"Tarea procesada correctamente: {tarea}")
    tarea_db = Tarea(titulo=tarea.titulo,contenido=tarea.contenido,creada=tarea.creada,realizada=tarea.realizada,caducada=tarea.caducada)
    Tarea.crear_tarea(tarea_db)
    