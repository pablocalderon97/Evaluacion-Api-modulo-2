from typing import Optional
from pydantic import BaseModel, Field, field_validator,model_validator
from sqlalchemy import Column, Integer, String, Boolean, Date , create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date


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
    creada = Column(Date,index=True)
    realizada = Column(Boolean, index=True)
    caducada = Column(Boolean,index=True)