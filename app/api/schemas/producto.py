from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    categoriaProducto_id: int
    precio: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    codigoBarra: Optional[str] = Field(None, max_length=50)
    activo: bool = True

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoriaProducto_id: Optional[int] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    codigoBarra: Optional[str] = None
    activo: Optional[bool] = None

class ProductoStockUpdate(BaseModel):
    """Para actualizar solo el stock"""
    stock: int = Field(..., ge=0)

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    categoriaProducto_id: int
    precio: float
    stock: int
    codigoBarra: Optional[str]
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True