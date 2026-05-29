from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.core.security import require_roles
from app.api.database.session import get_db
from app.api.repositories.finanzas_repository import FinanzasRepository

router = APIRouter(prefix="/finanzas", tags=["Finanzas"])

@router.get(
    "/ingresos",
    summary="Reporte de ingresos por período (membresías + tienda)",
)
def reporte_ingresos(
    fecha_inicio: datetime = Query(..., description="Fecha inicio (ISO 8601)"),
    fecha_fin:    datetime = Query(..., description="Fecha fin (ISO 8601)"),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    return FinanzasRepository.ingresos_por_periodo(db, fecha_inicio, fecha_fin)


@router.get(
    "/resumen",
    summary="Resumen de membresías activas y vencidas",
)
def resumen_membresias(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    return {
        "membresias_activas":  FinanzasRepository.clientes_con_membresia_activa(db),
        "membresias_vencidas": FinanzasRepository.clientes_con_membresia_vencida(db),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    } 
