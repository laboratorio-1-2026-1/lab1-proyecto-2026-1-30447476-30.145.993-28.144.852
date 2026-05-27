from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime

class ClienteBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    cedula: str = Field(..., max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    fechaNacimiento: Optional[date] = None

class ClienteCreate(ClienteBase):
    usuario_id: Optional[int] = None

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cedula: Optional[str] = None
    telefono: Optional[str] = None
    fechaNacimiento: Optional[date] = None
    activo: Optional[bool] = None

class ClienteResponse(ClienteBase):
    idCliente: int
    fechaRegistro: datetime
    activo: bool
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True