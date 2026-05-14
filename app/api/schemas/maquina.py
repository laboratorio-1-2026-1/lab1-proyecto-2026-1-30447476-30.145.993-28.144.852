from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class MaquinaCreate(BaseModel):
    nombreMaquina: str = Field(..., min_length=3)
    descripcionTecnica: Optional[str] = None
    categoria_id: int
    fechaAdquisicion: Optional[date] = None
    numeroSerie: Optional[str] = None

class MaquinaUpdate(BaseModel):
    nombreMaquina: Optional[str] = None
    descripcionTecnica: Optional[str] = None
    categoria_id: Optional[int] = None
    estadoOperativo: Optional[str] = None

class MaquinaEstadoUpdate(BaseModel):
    """Para actualizar solo el estado de la máquina"""
    estado_operativo: str = Field(..., description="Estado: Activa, En Mantenimiento, Fuera de Servicio")

class MaquinaResponse(BaseModel):
    idMaquinas: int
    nombreMaquina: str
    descripcionTecnica: Optional[str]
    estadoOperativo: str
    categoria_id: int
    fechaAdquisicion: Optional[date]
    created_at: datetime

class Config:
    from_attributes = True
