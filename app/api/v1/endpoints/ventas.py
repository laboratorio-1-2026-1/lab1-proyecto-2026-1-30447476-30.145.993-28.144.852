from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.services.venta_service import VentaService
from app.api.schemas.venta import VentaCreate

router = APIRouter(prefix="/tienda", tags=["Tienda (POS)"])

@router.post(
    "/ventas",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar venta (descuenta stock e impacta finanzas)",
)
def registrar_venta(
    data: VentaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    service = VentaService(db)
    resultado = service.registrar_venta(
        usuario_id=current_user["user_id"],
        cliente_id=data.cliente_id,
        items=[item.dict() for item in data.items],
        metodo_pago=data.metodoPago
    )
    return resultado

@router.get(
    "/ventas",
    summary="Listar historial de ventas",
)
def listar_ventas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    service = VentaService(db)
    ventas = service.listar_ventas(skip=skip, limit=limit)
    return {
        "status": "success",
        "mensaje": f"Se encontraron {len(ventas)} ventas.",
        "data": ventas
    }

@router.get(
    "/ventas/{venta_id}",
    summary="Ver detalle de una transacción",
)
def obtener_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    service = VentaService(db)
    venta = service.obtener_venta(venta_id)
    return {
        "status": "success",
        "mensaje": "Venta encontrada.",
        "data": venta
    }