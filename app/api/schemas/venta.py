from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class ItemVenta(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    precioUnitario: float = Field(..., gt=0)

class VentaCreate(BaseModel):
    cliente_id: Optional[int] = None
    items: List[ItemVenta]
    metodoPago: str

class VentaResponse(BaseModel):
    id: int
    numeroVenta: str
    fechaVenta: datetime
    montoTotal: float
    estado: str
    
    class Config:
        from_attributes = True