from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class CrearTarea(BaseModel):
    titulo: str = Field(..., min_length=5, description="Titulo de la tarea (mínimo 5 caracteres)")
    contenido: str = Field(..., description="Contenido de la tarea")
    creada: date = Field(..., description="Fecha de creación")
    realizada: Optional[bool] = Field(default=False, description="Estado de la tarea")
    caducada: Optional[bool] = Field(default=False, description="Si la tarea ha caducado")