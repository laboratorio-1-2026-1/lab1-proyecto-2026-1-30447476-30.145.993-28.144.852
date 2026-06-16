from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class SesionCreate(BaseModel):
    disciplina: str  # ← Lo convertiremos a disciplina_id en el endpoint
    entrenador_id: int
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    cupo_maximo: int

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
        from_attributes = True