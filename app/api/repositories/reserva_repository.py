from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models.reserva import Reserva
from app.api.models.sesion import Sesion


class ReservaRepository:
    @staticmethod
    def get_by_id(db: Session, reserva_id: int) -> Optional[Reserva]:
        return db.query(Reserva).filter(Reserva.id == reserva_id).first()

    @staticmethod
    def get_por_cliente(db: Session, cliente_id: int) -> List[Reserva]:
        return (
            db.query(Reserva)
            .filter(Reserva.cliente_id == cliente_id)
            .order_by(Reserva.fecha_reserva.desc())
            .all()
        )

    @staticmethod
    def existe_reserva_activa(db: Session, cliente_id: int, sesion_id: int) -> bool:
        return (
            db.query(Reserva)
            .filter(
                Reserva.cliente_id == cliente_id,
                Reserva.sesion_id == sesion_id,
                Reserva.estado == "Activa",
            )
            .first()
            is not None
        )

    @staticmethod
    def hay_solapamiento(db: Session, cliente_id: int, sesion: Sesion) -> bool:
        activas = (
            db.query(Reserva)
            .join(Sesion)
            .filter(
                Reserva.cliente_id == cliente_id,
                Reserva.estado == "Activa",
                Sesion.fecha == sesion.fecha,
                Sesion.hora_inicio < sesion.hora_fin,
                Sesion.hora_fin > sesion.hora_inicio,
            )
            .first()
        )
        return activas is not None

    @staticmethod
    def crear(db: Session, cliente_id: int, sesion_id: int) -> Reserva:
        sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
        if sesion and sesion.cupos_disponibles > 0:
            sesion.cupos_disponibles -= 1
        reserva = Reserva(
            cliente_id=cliente_id,
            sesion_id=sesion_id,
            fecha_reserva=datetime.now(),
            estado="Activa",
        )
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def cancelar(db: Session, reserva_id: int) -> Optional[Reserva]:
        reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            return None
        if reserva.estado != "Cancelada":
            sesion = db.query(Sesion).filter(Sesion.id == reserva.sesion_id).first()
            if sesion:
                sesion.cupos_disponibles += 1
            reserva.estado = "Cancelada"
            db.commit()
            db.refresh(reserva)
        return reserva


reserva_repository = ReservaRepository()
