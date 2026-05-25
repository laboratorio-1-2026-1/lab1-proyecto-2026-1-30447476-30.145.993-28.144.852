from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class RolOut(BaseModel):
    idRol:       int
    nombreRol:   str
    descripcion: Optional[str] = None
    model_config = {"from_attributes": True}


class RegisterRequest(BaseModel):
    nombreUsuario: str      = Field(..., min_length=3, max_length=100)
    email:         EmailStr
    password:      str      = Field(..., min_length=8)
    rol_id:        int      = Field(default=4)
    cedula:        Optional[str] = Field(default=None, max_length=20)  # NUEVO


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class UsuarioCreate(BaseModel):
    nombreUsuario: str      = Field(..., min_length=3, max_length=100)
    email:         EmailStr
    password:      str      = Field(..., min_length=8)
    rol_id:        int
    cedula:        Optional[str] = None  # NUEVO


class UsuarioUpdate(BaseModel):
    nombreUsuario: Optional[str]      = None
    email:         Optional[EmailStr] = None
    rol_id:        Optional[int]      = None
    activo:        Optional[bool]     = None
    cedula:        Optional[str]      = None  # NUEVO


class UsuarioOut(BaseModel):
    idUsuarios:    int
    nombreUsuario: str
    email:         str
    cedula:        Optional[str] = None  # NUEVO
    rol_id:        int
    activo:        bool
    created_at:    datetime
    rol:           Optional[RolOut] = None
    model_config = {"from_attributes": True}