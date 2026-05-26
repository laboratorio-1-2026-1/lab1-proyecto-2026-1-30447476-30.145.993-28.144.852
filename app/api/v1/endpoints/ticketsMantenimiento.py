from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.core.errors import conflict_response
from app.api.schemas.ticketsMantenimiento import (
    TicketCreate,
    TicketResolve,
    TicketResponse,
)
from app.api.repositories.maquina_repository import MaquinaRepository
from app.api.repositories.ticketsMantenimiento_repository import TicketsMantenimientoRepository

router = APIRouter(prefix="/tickets-mantenimiento", tags=["Máquinas e Instalaciones"])


@router.get(
    "/maquinas/{maquina_id}/tickets",
    response_model=List[TicketResponse],
    summary="Historial de tickets de mantenimiento de una máquina",
)
def listar_tickets(
    maquina_id: int,
    skip: int = 0,               
    limit: int = 100,            
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    if not MaquinaRepository.get_by_id(db, maquina_id):
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return TicketsMantenimientoRepository.get_by_maquina(
        db, maquina_id, skip=skip, limit=limit   
    )


@router.post(
    "/tickets-mantenimiento",
    response_model=TicketResponse,
    status_code=201,
    summary="Abrir ticket de mantenimiento (cambia máquina a 'En Mantenimiento')",
)
def abrir_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    if not MaquinaRepository.get_by_id(db, data.maquina_id):
        raise HTTPException(status_code=404, detail="Máquina no encontrada")

    # Aviso si ya hay un ticket abierto para esa máquina (no bloqueante, pero informativo)
    if TicketsMantenimientoRepository.exists_abierto_para_maquina(db, data.maquina_id):
        return conflict_response(
            "ERR_TICKET_YA_ABIERTO",
            "La máquina ya tiene un ticket de mantenimiento abierto.",
        )

    return TicketsMantenimientoRepository.create(
        db,
        maquina_id=data.maquina_id,
        usuario_id=current_user["user_id"],
        descripcionFalla=data.descripcionFalla,
        tecnicoResponsable=data.tecnicoResponsable,
    )


@router.patch(
    "/tickets-mantenimiento/{ticket_id}/resolver",
    response_model=TicketResponse,
    summary="Cerrar ticket y rehabilitar máquina a 'Activa'",
)
def resolver_ticket(
    ticket_id: int,
    data: TicketResolve,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),   # ← typo corregido
):
    ticket = TicketsMantenimientoRepository.get_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if ticket.estado == "Resuelto":
        return conflict_response(
            "ERR_TICKET_YA_RESUELTO",
            "Este ticket ya fue resuelto anteriormente.",
        )

    return TicketsMantenimientoRepository.resolver(
        db,
        ticket_id=ticket_id,
        fechaResolucion=data.fechaResolucion,
        costoReparacion=data.costoReparacion,
        tecnicoResponsable=data.tecnicoResponsable,
    )