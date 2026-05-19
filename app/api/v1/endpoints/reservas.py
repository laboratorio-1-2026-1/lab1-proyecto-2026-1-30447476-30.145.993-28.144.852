from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.database.session import get_db
from app.api.schemas.reserva import ReservaCreate, ReservaResponse
from app.api.services.reserva_service import reserva_service

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("", response_model=List[ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    return reserva_service.listar_todas(db)


@router.get("/cliente/{cliente_id}", response_model=List[ReservaResponse])
def listar_reservas_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return reserva_service.listar_por_cliente(db, cliente_id)


@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    return reserva_service.crear(db, reserva.cliente_id, reserva.sesion_id)


@router.delete("/{reserva_id}", response_model=ReservaResponse)
def cancelar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    return reserva_service.cancelar(db, reserva_id)
