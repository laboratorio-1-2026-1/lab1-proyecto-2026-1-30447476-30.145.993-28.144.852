from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
from app.api.models.maquina import EstadoMaquina
from app.api.repositories.ticketsMantenimiento_repository import TicketsMantenimientoRepository
from app.api.services.maquina_service import MaquinaService
from app.api.schemas.ticketsMantenimiento import TicketCreate, TicketResolve


def _error_404(codigo: str, mensaje: str):
    return HTTPException(status_code=404, detail={"error": "Not Found", "codigoInterno": codigo, "mensaje": mensaje, "timestamp": datetime.now(timezone.utc).isoformat()})

def _error_409(codigo: str, mensaje: str):
    return HTTPException(status_code=409, detail={"error": "Conflict", "codigoInterno": codigo, "mensaje": mensaje, "timestamp": datetime.now(timezone.utc).isoformat()})

def _serializar_ticket(t) -> dict:
    return {
        "id": t.id,
        "maquina_id": t.maquina_id,
        "descripcionFalla": getattr(t, "descripcionFalla", None),
        "estado": t.estado,
        "tecnicoResponsable": getattr(t, "tecnicoResponsable", None),
        "costoReparacion": float(t.costoReparacion) if getattr(t, "costoReparacion", None) else None,
        "fechaApertura": t.fechaReporte.isoformat() if getattr(t, "fechaReporte", None) else None,
        "fechaResolucion": t.fechaResolucion.isoformat() if getattr(t, "fechaResolucion", None) else None,
    }


class MantenimientoService:
    def __init__(self, db: Session):
        self.repo = TicketsMantenimientoRepository(db)
        self.maquina_service = MaquinaService(db)

    def abrir_ticket(self, maquina_id: int, data: TicketCreate):
        try:
            maquina = self.maquina_service.obtener(maquina_id)
        except HTTPException as e:
            if e.status_code == 404:
                raise _error_404("ERR_MAQUINA_NO_ENCONTRADA", f"Máquina con ID {maquina_id} no encontrada.")
            raise e

        if self.repo.get_abiertos_by_maquina(maquina_id):
            raise _error_409("ERR_TICKET_ABIERTO_EXISTENTE", f"La máquina con ID {maquina_id} ya tiene un ticket abierto. Resuélvalo antes de crear uno nuevo.")

        ticket = self.repo.create(
            maquina_id=maquina_id,
            usuario_id=getattr(data, "usuario_id", None),
            descripcionFalla=data.descripcionFalla,
            tecnicoResponsable=getattr(data, "tecnicoResponsable", None),
            costoReparacion=getattr(data, "costoReparacion", None),
        )

        estado_actual = maquina.get("data", {}).get("estado") if isinstance(maquina, dict) else getattr(maquina, "estadoOperativo", None)
        if estado_actual in (EstadoMaquina.ACTIVA, "Activa"):
            self.maquina_service.cambiar_estado(maquina_id, EstadoMaquina.EN_MANTENIMIENTO)

        return {"status": "success", "mensaje": "Ticket creado. Máquina marcada como EN MANTENIMIENTO.", "data": _serializar_ticket(ticket)}

    def listar_por_maquina(self, maquina_id: int):
        try:
            self.maquina_service.obtener(maquina_id)
        except HTTPException as e:
            if e.status_code == 404:
                raise _error_404("ERR_MAQUINA_NO_ENCONTRADA", f"Máquina con ID {maquina_id} no encontrada.")
            raise e
        tickets = self.repo.get_by_maquina(maquina_id)
        return {"status": "success", "mensaje": f"{len(tickets)} ticket(s) encontrados.", "data": [_serializar_ticket(t) for t in tickets]}

    def obtener_ticket(self, ticket_id: int):
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise _error_404("ERR_TICKET_NO_ENCONTRADO", f"Ticket con ID {ticket_id} no encontrado.")
        return {"status": "success", "mensaje": "Ticket encontrado.", "data": _serializar_ticket(ticket)}

    def resolver_ticket(self, ticket_id: int, data: TicketResolve):
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise _error_404("ERR_TICKET_NO_ENCONTRADO", f"Ticket con ID {ticket_id} no encontrado.")
        if ticket.estado == "Cerrado":
            raise _error_409("ERR_TICKET_YA_CERRADO", f"El ticket con ID {ticket_id} ya está cerrado.")

        ticket_actualizado = self.repo.resolver(
            ticket_id=ticket_id,
            costoReparacion=getattr(data, "costoReparacion", None),
            tecnicoResponsable=getattr(data, "tecnicoResponsable", None),
        )
        if not ticket_actualizado:
            raise _error_404("ERR_TICKET_NO_ENCONTRADO", f"Ticket con ID {ticket_id} no encontrado al resolver.")

        if self.repo.count_abiertos_by_maquina(ticket.maquina_id) == 0:
            self.maquina_service.cambiar_estado(ticket.maquina_id, EstadoMaquina.ACTIVA)

        return {"status": "success", "mensaje": "Ticket resuelto. Máquina rehabilitada como ACTIVA.", "data": _serializar_ticket(ticket_actualizado)}
