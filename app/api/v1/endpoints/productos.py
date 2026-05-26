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
from app.api.repositories.producto_repository import ProductoRepository
from app.api.repositories.categoriaProducto_repository import CategoriaProductoRepository

router = APIRouter(prefix="/tienda/productos", tags=["Tienda (POS)"])

@router.get("/productos", response_model=List[ProductoResponse])
def listar_productos(
    categoria_id: Optional[int] = None,
    solo_activos: bool = True,
    skip: int = 0,               
    limit: int = 100,            
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas", "Entrenador")),
):
    return ProductoRepository.get_all(
        db,
        solo_activos=solo_activos,
        categoria_id=categoria_id,
        skip=skip,                
        limit=limit               
    )

@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    data: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    if data.stock < 0:
        return bad_request_response("ERR_STOCK_NEGATIVO", "El stock no puede ser negativo.")
    
    return ProductoRepository.create(db, data)

@router.get("/productos/{producto_id}", response_model=ProductoResponse)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    producto = ProductoRepository.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.patch("/productos/{producto_id}/stock", response_model=ProductoResponse)
def ajustar_stock(
    producto_id: int,
    data: ProductoStockUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    if data.stock < 0:
        return bad_request_response("ERR_STOCK_NEGATIVO", "El stock no puede ser negativo.")
    
    producto = ProductoRepository.update_stock(db, producto_id, data.stock)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/productos/{producto_id}", status_code=200)
def desactivar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    producto = ProductoRepository.desactivar(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"status": "success", "mensaje": "Producto desactivado correctamente"}