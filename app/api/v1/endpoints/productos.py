from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.core.errors import conflict_response, bad_request_response
from app.api.schemas.producto import (
    ProductoCreate,
    ProductoUpdate,
    ProductoStockUpdate,
    ProductoResponse,
)
from app.api.services.producto_service import ProductoService

router = APIRouter(prefix="/tienda/productos", tags=["Tienda (POS)"])

@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    categoria_id: Optional[int] = None,
    solo_activos: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas", "Entrenador")),
):
    service = ProductoService(db)
    resultado = service.listar(activo=solo_activos, skip=skip, limit=limit)
    return resultado["data"]

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    data: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    if data.stock < 0:
        return bad_request_response("ERR_STOCK_NEGATIVO", "El stock no puede ser negativo.")
    
    service = ProductoService(db)
    resultado = service.crear(data)
    return resultado["data"]

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    service = ProductoService(db)
    resultado = service.obtener(producto_id)
    return resultado["data"]

@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
def ajustar_stock(
    producto_id: int,
    data: ProductoStockUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    if data.stock < 0:
        return bad_request_response("ERR_STOCK_NEGATIVO", "El stock no puede ser negativo.")
    
    service = ProductoService(db)
    resultado = service.actualizar_stock(producto_id, data.stock)
    return resultado["data"]

@router.delete("/{producto_id}", status_code=200)
def desactivar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    service = ProductoService(db)
    resultado = service.eliminar(producto_id)
    return resultado