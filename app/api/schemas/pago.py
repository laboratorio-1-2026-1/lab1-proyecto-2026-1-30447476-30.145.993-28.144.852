from pydantic import BaseModel
from datetime import datetime

# Schema para crear un pago
class PagoCreate(BaseModel):
    cliente_id: int
    plan_id: int
    monto: float
    fecha_pago: datetime
    fecha_vencimiento: datetime

# Schema para responder con pago
class PagoResponse(BaseModel):
    id: int
    cliente_id: int
    plan_id: int
    monto: float
    fecha_pago: datetime
    fecha_vencimiento: datetime

    class Config:
        from_attributes = True