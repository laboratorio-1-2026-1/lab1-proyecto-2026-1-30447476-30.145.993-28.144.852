from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.core.errors import bad_request_response, conflict_response
from app.api.schemas.venta import (
    VentaCreate,
    VentaResponse,
)
from app.api.repositories.producto_repository import ProductoRepository
from app.api.repositories.venta_repository import VentaRepository

router = APIRouter(prefix="/tienda", tags=["Tienda (POS)"])

@router.post(
    "/ventas",
    response_model=VentaResponse,
    status_code=201,
    summary="Registrar venta (descuenta stock e impacta finanzas)",
)
def registrar_venta(
    data: VentaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    if not data.items:
        return bad_request_response(
            "ERR_VENTA_SIN_ITEMS",
            "La venta debe incluir al menos un producto.",
        )

    # Validar stock de todos los ítems ANTES de persistir (regla de negocio: sin sobreventa)
    for item in data.items:
        if item.cantidad <= 0:
            return bad_request_response(
                "ERR_CANTIDAD_INVALIDA",
                f"La cantidad del producto {item.producto_id} debe ser mayor a 0.",
            )

        producto = ProductoRepository.get_by_id(db, item.producto_id)
        if not producto:
            raise HTTPException(
                status_code=404,
                detail=f"Producto con id {item.producto_id} no encontrado",
            )
        if not producto.activo:
            return bad_request_response(
                "ERR_PRODUCTO_INACTIVO",
                f"El producto '{producto.nombre}' no está disponible para la venta.",
            )
        if producto.stock < item.cantidad:
            return conflict_response(
                "ERR_STOCK_INSUFICIENTE",
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock}, solicitado: {item.cantidad}.",
            )

    items_dict = [{"producto_id": i.producto_id, "cantidad": i.cantidad} for i in data.items]

    return VentaRepository.create(
        db,
        usuario_id=current_user["user_id"],
        items=items_dict,
        cliente_id=data.cliente_id,
        metodoPago=data.metodoPago,
    )


@router.get(
    "/ventas",
    response_model=List[VentaResponse],
    summary="Listar historial de ventas",
)
def listar_ventas(
    skip: int = 0,               
    limit: int = 100,            
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    return VentaRepository.get_all(
        db,
        skip=skip,               
        limit=limit               
    )


@router.get(
    "/ventas/{venta_id}",
    response_model=VentaResponse,
    summary="Ver detalle de una transacción",
)
def obtener_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    venta = VentaRepository.get_by_id(db, venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta