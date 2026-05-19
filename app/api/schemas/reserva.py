from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema para crear una reserva
class ReservaCreate(BaseModel):
    cliente_id: int
    sesion_id: int

# Schema para responder con datos de reserva
class ReservaResponse(BaseModel):
    id: int
    cliente_id: int
    sesion_id: int
    fecha_reserva: datetime

    class Config:
        from_attributes = True