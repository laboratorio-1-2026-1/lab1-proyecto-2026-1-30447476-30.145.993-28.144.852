from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class EntrenadorBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    cedula: str = Field(..., max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[EmailStr] = None
    especialidad: Optional[str] = Field(None, max_length=100)

class EntrenadorCreate(EntrenadorBase):
    usuario_id: Optional[int] = None

class EntrenadorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cedula: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    especialidad: Optional[str] = None
    activo: Optional[bool] = None

class EntrenadorResponse(EntrenadorBase):
    idEntrenador: int
    activo: bool
    usuario_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True