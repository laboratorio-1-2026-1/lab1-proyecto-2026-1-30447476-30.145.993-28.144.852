from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EvaluacionBase(BaseModel):
    cliente_id: int
    entrenador_id: int
    fechaEvaluacion: Optional[datetime] = None
    peso: Optional[float] = Field(None, gt=0)
    estatura: Optional[float] = Field(None, gt=0)
    porcentajeGrasa: Optional[float] = Field(None, ge=0, le=100)
    masaMuscular: Optional[float] = Field(None, gt=0)
    observaciones: Optional[str] = None

class EvaluacionCreate(EvaluacionBase):
    pass

class EvaluacionUpdate(BaseModel):
    fechaEvaluacion: Optional[datetime] = None
    peso: Optional[float] = Field(None, gt=0)
    estatura: Optional[float] = Field(None, gt=0)
    porcentajeGrasa: Optional[float] = Field(None, ge=0, le=100)
    masaMuscular: Optional[float] = Field(None, gt=0)
    observaciones: Optional[str] = None

class EvaluacionResponse(EvaluacionBase):
    idEvaluacionesBiometricas: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True