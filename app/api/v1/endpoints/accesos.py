from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.core.security import require_roles
from app.api.database.session import get_db
from app.api.schemas.acceso import AccesoCreate, AccesoResponse
from app.api.services.acceso_service import acceso_service

router = APIRouter(prefix="/accesos", tags=["Accesos"])


@router.get(
    "",
    response_model=List[AccesoResponse],
    summary="Listar todos los accesos (Solo Admin)",
)
def listar_accesos(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return acceso_service.listar(db)


@router.get(
    "/cliente/{cliente_id}",
    response_model=List[AccesoResponse],
    summary="Historial de accesos de un cliente",
)
def listar_accesos_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    return acceso_service.listar_por_cliente(db, cliente_id)


@router.post(
    "/entrada",
    response_model=AccesoResponse,
    summary="Registrar entrada por cédula — valida membresía vigente",
)
def registrar_entrada(datos: AccesoCreate, db: Session = Depends(get_db)):
    """
    Endpoint del torniquete/recepción.
    Recibe la cédula del cliente y valida membresía activa.
    No requiere token JWT — es el punto de entrada físico del gimnasio.
    """
    return acceso_service.registrar_entrada(db, datos.documento_identidad)