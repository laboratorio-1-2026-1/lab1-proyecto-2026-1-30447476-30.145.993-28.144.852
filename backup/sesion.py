from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

# Schema para crear una sesión (lo que recibe la API)
class SesionCreate(BaseModel):
    disciplina: str
    entrenador_id: int
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    cupo_maximo: int

# Schema para responder con datos de sesión (lo que devuelve la API)
class SesionResponse(BaseModel):
    id: int
    disciplina: str
    entrenador_id: int
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    cupo_maximo: int
    cupos_disponibles: int

    class Config:
        from_attributes = True  # Para SQLAlchemy