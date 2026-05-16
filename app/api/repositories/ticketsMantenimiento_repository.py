from datetime import date
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.ticketsMantenimiento import TicketsMantenimiento
from app.api.models.maquina import Maquina


class TicketsMantenimientoRepository:

    @staticmethod
    def get_all(db: Session) -> List[TicketsMantenimiento]:
        return db.query(TicketsMantenimiento).order_by(
            TicketsMantenimiento.fechaReporte.desc()
        ).all()

    @staticmethod
    def get_by_id(db: Session, ticket_id: int) -> Optional[TicketsMantenimiento]:
        return db.query(TicketsMantenimiento).filter(
            TicketsMantenimiento.idTicketsMantenimiento == ticket_id
        ).first()

    @staticmethod
    def get_by_maquina(db: Session, maquina_id: int) -> List[TicketsMantenimiento]:
        return db.query(TicketsMantenimiento).filter(
            TicketsMantenimiento.maquina_id == maquina_id
        ).order_by(TicketsMantenimiento.fechaReporte.desc()).all()

    @staticmethod
    def get_abiertos(db: Session) -> List[TicketsMantenimiento]:
        return db.query(TicketsMantenimiento).filter(
            TicketsMantenimiento.estado == "Abierto"
        ).order_by(TicketsMantenimiento.fechaReporte.desc()).all()

    @staticmethod
    def create(
        db: Session,
        maquina_id: int,
        usuario_id: int,
        descripcionFalla: str,
        tecnicoResponsable: Optional[str] = None,
    ) -> TicketsMantenimiento:
        ticket = TicketsMantenimiento(
            maquina_id=maquina_id,
            usuario_id=usuario_id,
            descripcionFalla=descripcionFalla,
            tecnicoResponsable=tecnicoResponsable,
            estado="Abierto",
        )
        # Regla de negocio: cambiar estado de la máquina a "En Mantenimiento"
        maquina = db.query(Maquina).filter(Maquina.idMaquinas == maquina_id).first()
        if maquina:
            maquina.estadoOperativo = "En Mantenimiento"

        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def resolver(
        db: Session,
        ticket_id: int,
        fechaResolucion: date,
        costoReparacion: Optional[Decimal] = None,
        tecnicoResponsable: Optional[str] = None,
    ) -> Optional[TicketsMantenimiento]:
        ticket = TicketsMantenimientoRepository.get_by_id(db, ticket_id)
        if not ticket:
            return None

        ticket.fechaResolucion = fechaResolucion
        ticket.costoReparacion = costoReparacion
        if tecnicoResponsable:
            ticket.tecnicoResponsable = tecnicoResponsable
        ticket.estado = "Resuelto"

        # Regla de negocio: rehabilitar máquina a "Activa"
        maquina = db.query(Maquina).filter(Maquina.idMaquinas == ticket.maquina_id).first()
        if maquina:
            maquina.estadoOperativo = "Activa"
            maquina.ultimoMantenimiento = fechaResolucion

        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def exists_abierto_para_maquina(db: Session, maquina_id: int) -> bool:
        return db.query(TicketsMantenimiento).filter(
            TicketsMantenimiento.maquina_id == maquina_id,
            TicketsMantenimiento.estado == "Abierto",
        ).first() is not None 