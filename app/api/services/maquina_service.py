from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.models import Maquina, CategoriaMaquina, TicketMantenimiento
from app.schemas.schemas import (
    MaquinaCreate, MaquinaUpdate, MaquinaEstadoUpdate,
    TicketCreate, TicketResolverRequest,
    CategoriaMaquinaCreate,
)


class MaquinaService:

    @staticmethod
    def list_maquinas(db: Session, categoria_id: int = None, estado: str = None):
        q = db.query(Maquina)
        if categoria_id:
            q = q.filter(Maquina.categoria_id == categoria_id)
        if estado:
            q = q.filter(Maquina.estadoOperativo == estado)
        return q.all()

    @staticmethod
    def get_maquina(db: Session, maquina_id: int) -> Maquina:
        m = db.query(Maquina).filter(Maquina.idMaquinas == maquina_id).first()
        if not m:
            raise HTTPException(status_code=404, detail="Máquina no encontrada")
        return m

    @staticmethod
    def create_maquina(db: Session, data: MaquinaCreate) -> Maquina:
        cat = db.query(CategoriaMaquina).filter(
            CategoriaMaquina.idCategoriasMaquinas == data.categoria_id
        ).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

        if data.numeroSerie:
            dup = db.query(Maquina).filter(Maquina.numeroSerie == data.numeroSerie).first()
            if dup:
                raise HTTPException(status_code=409, detail="Número de serie ya registrado")

        m = Maquina(**data.model_dump())
        db.add(m)
        db.commit()
        db.refresh(m)
        return m

    @staticmethod
    def update_maquina(db: Session, maquina_id: int, data: MaquinaUpdate) -> Maquina:
        m = MaquinaService.get_maquina(db, maquina_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(m, field, value)
        db.commit()
        db.refresh(m)
        return m

    @staticmethod
    def update_estado(db: Session, maquina_id: int, data: MaquinaEstadoUpdate) -> Maquina:
        valid_states = ["Activa", "En Mantenimiento", "Fuera de Servicio"]
        if data.estadoOperativo not in valid_states:
            raise HTTPException(
                status_code=400,
                detail=f"Estado inválido. Opciones: {valid_states}"
            )
        m = MaquinaService.get_maquina(db, maquina_id)
        m.estadoOperativo = data.estadoOperativo
        db.commit()
        db.refresh(m)
        return m

    # Categorias

    @staticmethod
    def list_categorias(db: Session):
        return db.query(CategoriaMaquina).all()

    @staticmethod
    def create_categoria(db: Session, data: CategoriaMaquinaCreate) -> CategoriaMaquina:
        c = CategoriaMaquina(**data.model_dump())
        db.add(c)
        db.commit()
        db.refresh(c)
        return c


class TicketService:

    @staticmethod
    def list_tickets(db: Session, maquina_id: int):
        return db.query(TicketMantenimiento).filter(
            TicketMantenimiento.maquina_id == maquina_id
        ).order_by(TicketMantenimiento.fechaReporte.desc()).all()

    @staticmethod
    def create_ticket(db: Session, data: TicketCreate, usuario_id: int) -> TicketMantenimiento:
        m = db.query(Maquina).filter(Maquina.idMaquinas == data.maquina_id).first()
        if not m:
            raise HTTPException(status_code=404, detail="Máquina no encontrada")

        ticket = TicketMantenimiento(
            maquina_id=data.maquina_id,
            usuario_id=usuario_id,
            descripcionFalla=data.descripcionFalla,
            tecnicoResponsable=data.tecnicoResponsable,
            estado="Abierto",
        )
        # Cambiar estado de la máquina
        m.estadoOperativo = "En Mantenimiento"
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def resolver_ticket(
        db: Session, ticket_id: int, data: TicketResolverRequest
    ) -> TicketMantenimiento:
        ticket = db.query(TicketMantenimiento).filter(
            TicketMantenimiento.idTicketsMantenimiento == ticket_id
        ).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        if ticket.estado == "Resuelto":
            raise HTTPException(status_code=409, detail="El ticket ya está resuelto")

        ticket.fechaResolucion = data.fechaResolucion
        ticket.costoReparacion = data.costoReparacion
        if data.tecnicoResponsable:
            ticket.tecnicoResponsable = data.tecnicoResponsable
        ticket.estado = "Resuelto"

        # Rehabilitar máquina
        maquina = db.query(Maquina).filter(Maquina.idMaquinas == ticket.maquina_id).first()
        if maquina:
            maquina.estadoOperativo = "Activa"
            maquina.ultimoMantenimiento = data.fechaResolucion

        db.commit()
        db.refresh(ticket)
        return ticket