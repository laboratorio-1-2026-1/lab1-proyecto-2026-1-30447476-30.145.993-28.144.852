from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DisciplinaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    duracionMinutos: Optional[int] = None

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    duracionMinutos: Optional[int] = None

class DisciplinaResponse(DisciplinaBase):
    idDisciplina: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True