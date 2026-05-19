from pydantic import BaseModel
from datetime import datetime

# Schema para registrar entrada (solo cédula)
class AccesoCreate(BaseModel):
    documento_identidad: str  # Cédula del cliente

# Schema para responder con registro de acceso
class AccesoResponse(BaseModel):
    id: int
    cliente_id: int
    fecha_hora_entrada: datetime
    mensaje: str

    class Config:
        from_attributes = True