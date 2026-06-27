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

# Creacion API

app = FastAPI(
    title="Evaluacion modulo programacion avanzada, api con tareas a realizar",
    description="API de ejemplo con base de datos SQLite.",
    version="1.0.0"
)

# EndPoints

@app.post("/tasks/")
def crear_tarea(datos: CrearTarea):
    return Tarea.crear_tarea(datos.titulo, datos.contenido, datos.creada, datos.realizada, datos.caducada)

@app.get("/tasks/all")
def listar_tareas():
    return Tarea.listar_tareas()

@app.get("/tasks/{id}")
def obtener_tarea(id: int):
    return Tarea.obtener_por_id(id)

@app.put("/tasks/{id}/realizada")
def marcar_realizada(id: int):
    return Tarea.tarea_realizada(id)

@app.get("/tasks/caducadas/")
def comprobar_caducadas():
    return Tarea.comprobar_caducadas(date.today())