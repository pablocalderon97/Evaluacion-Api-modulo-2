import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator,model_validator
from datetime import datetime, date
from modelsdb import CrearTarea
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

@app.post("/tasks/",status_code=201)
def crear_tarea(datos: CrearTarea):

    if datos.creada > date.today():
        raise HTTPException(status_code=400, detail="La fecha de creación no puede ser futura")

    if datos.deadline and datos.deadline < datos.creada:
        raise HTTPException(status_code=400, detail="El deadline no puede ser anterior a la fecha de creación de la tarea")
    
    return Tarea.crear_tarea(datos.titulo, datos.contenido, datos.creada, datos.deadline, datos.realizada, datos.caducada)

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