from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema para crear una evaluación biométrica
class EvaluacionCreate(BaseModel):
    peso: float
    estatura: float
    grasa_corporal: Optional[float] = None
    observaciones: Optional[str] = None

# Schema para responder con evaluación
class EvaluacionResponse(BaseModel):
    id: int
    cliente_id: int
    entrenador_id: int
    peso: float
    estatura: float
    grasa_corporal: Optional[float]
    observaciones: Optional[str]
    fecha: datetime

    class Config:
        from_attributes = True