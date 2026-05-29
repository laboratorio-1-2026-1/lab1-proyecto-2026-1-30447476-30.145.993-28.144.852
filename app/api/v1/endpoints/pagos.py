from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.schemas.pago import PagoCreate, PagoResponse
from app.api.repositories.pago_repository import PagoRepository
from app.api.repositories.plan_repository import PlanRepository
from app.api.repositories.cliente_repository import ClienteRepository

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.post("", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pago(
    data: PagoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    cliente = ClienteRepository.get_by_id(db, data.cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    plan = PlanRepository.get_by_id(db, data.plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan no encontrado")

    return PagoRepository.create(db, data)


@router.get("", response_model=List[PagoResponse])
def listar_pagos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    return PagoRepository.get_all(db)


@router.get("/{pago_id}", response_model=PagoResponse)
def obtener_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    pago = PagoRepository.get_by_id(db, pago_id)
    if not pago:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return pago


@router.get("/cliente/{cliente_id}", response_model=List[PagoResponse])
def listar_pagos_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Finanzas")),
):
    cliente = ClienteRepository.get_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return PagoRepository.get_by_cliente(db, cliente_id)
