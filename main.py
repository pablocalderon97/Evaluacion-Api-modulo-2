import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator,model_validator
from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from taskmanager import Tarea

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Setup DB

DATABASE_URL = "sqlite:///./tareas.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class CrearTarea(BaseModel):
    id: Optional[int] = None
    titulo: str = Field(..., min_length=5, description="Titulo de la tarea a realizar (minimo 5 caracteres)")
    contenido: str = Field(..., description="Contenido de la tarea a realizar")
    creada: date = Field(...,description="Fecha de la creacion de la tarea")
    realizada: Optional[bool] = Field(default=False,description="Estado de la tarea") # Lo inicializo a falso para luego poder cambiarlo en BD con PUT una vez completada la tarea
    caducada: Optional[bool] = Field(default=False,description="Estado si la tarea a caducado o no") # Lo inicializo a falso para luego comprobarlo con GET

class TareaDB(Base):
    __tablename__ = "tareas"

    id = Column(Integer,primary_key=True, index=True)
    titulo = Column(String, index=True)
    contenido = Column(String, index=True)
    fecha = Column(Date,index=True)
    realizada = Column(Boolean, index=True)
    caducada = Column(Boolean,index=True)

# Creacion API

app = FastAPI(
    title="Evaluacion modulo programacion avanzada, api con tareas a realizar",
    description="API de ejemplo con base de datos SQLite.",
    version="1.0.0"
)

# EndPoints

@app.get("/tasks/{id}",response_model=TareaDB)
def listar_tareas(tarea:CrearTarea,id:int):

    Tarea.obtener_tarea_id(tarea,id)
    
@app.get("/tasks/caducadas")
def tareas_caducadas(tarea:CrearTarea):

    fecha_actual = date.today()
    Tarea.comprobar_tareas_caducadas(tarea,fecha_actual)

@app.put("/tasks/{id}/completada",response_model=TareaDB)
def completar_tarea(tarea:CrearTarea,id:int):

    Tarea.tarea_realizada(tarea,id)

@app.post("/tasks/",response_model=TareaDB,status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea:CrearTarea):
    
    logging.info(f"Tarea procesada correctamente: {tarea}")
    tarea_db = TareaDB(id = tarea.id,titulo=tarea.titulo,contenido=tarea.contenido,creada=tarea.creada,realizada=tarea.realizada,caducada=tarea.caducada)
    Tarea.crear_tarea(tarea_db)
    