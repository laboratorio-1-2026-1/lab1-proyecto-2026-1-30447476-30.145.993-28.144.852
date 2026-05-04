from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombreUsuario: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    rol_id: int

class UsuarioCreate(UsuarioBase):
    password: str = Field(
        ...,
        min_length=8,
        description="Mínimo 8 caracteres"
    )

class UsuarioResponse(UsuarioBase):
    idUsuarios: int
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    usuario: UsuarioResponse
    mensaje: str = "Login exitoso"