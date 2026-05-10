from pydantic import BaseModel
from typing import Optional

# Schema para crear un plan
class PlanCreate(BaseModel):
    nombre: str
    precio: float
    duracion_dias: int

# Schema para responder con plan
class PlanResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    duracion_dias: int

    class Config:
        from_attributes = True