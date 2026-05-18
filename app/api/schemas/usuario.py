from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class RolOut(BaseModel):
    idRol:      int
    nombreRol:  str
    descripcion: Optional[str] = None
    model_config = {"from_attributes": True}


class RegisterRequest(BaseModel):
    nombreUsuario: str      = Field(..., min_length=3, max_length=100)
    email:         EmailStr
    password:      str      = Field(..., min_length=8)
    rol_id:        int      = Field(default=4)


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class UsuarioCreate(BaseModel):
    nombreUsuario: str      = Field(..., min_length=3, max_length=100)
    email:         EmailStr
    password:      str      = Field(..., min_length=8)
    rol_id:        int


class UsuarioUpdate(BaseModel):
    nombreUsuario: Optional[str]      = None
    email:         Optional[EmailStr] = None
    rol_id:        Optional[int]      = None
    activo:        Optional[bool]     = None


class UsuarioOut(BaseModel):
    idUsuarios:    int
    nombreUsuario: str
    email:         str
    rol_id:        int
    activo:        bool
    created_at:    datetime
    rol:           Optional[RolOut] = None
    model_config = {"from_attributes": True}