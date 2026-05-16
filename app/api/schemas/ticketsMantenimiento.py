from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TicketCreate(BaseModel):
    maquina_id: int
    descripcionFalla: str = Field(..., min_length=10, max_length=500)
    tecnicoResponsable: Optional[str] = None

class TicketResolve(BaseModel):
    fechaResolucion: datetime
    costoReparacion: Optional[float] = None
    tecnicoResponsable: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    maquina_id: int
    descripcionFalla: str
    estado: str
    fechaReporte: datetime 
    fechaResolucion: Optional[datetime] = None
    costoReparacion: Optional[float] = None
    tecnicoResponsable: Optional[str] = None

    class Config:
        from_attributes = True