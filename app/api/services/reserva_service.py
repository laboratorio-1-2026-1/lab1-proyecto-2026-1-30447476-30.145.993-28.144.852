from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.models.reserva import Reserva
from app.api.repositories.cliente_repository import cliente_repository
from app.api.repositories.reserva_repository import reserva_repository
from app.api.repositories.sesion_repository import sesion_repository


class ReservaService:
    def listar_todas(self, db: Session) -> List[Reserva]:
        return (
            db.query(Reserva)
            .order_by(Reserva.fecha_reserva.desc())
            .all()
        )

    def listar_por_cliente(self, db: Session, cliente_id: int) -> List[Reserva]:
        return reserva_repository.get_por_cliente(db, cliente_id)

    def obtener(self, db: Session, reserva_id: int) -> Reserva:
        r = reserva_repository.get_by_id(db, reserva_id)
        if not r:
            raise HTTPException(status_code=404, detail="Reserva no encontrada.")
        return r

    def crear(self, db: Session, cliente_id: int, sesion_id: int) -> Reserva:
        cliente = cliente_repository.get_by_id(db, cliente_id)
        if not cliente or not cliente.activo:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado o inactivo.",
            )

        sesion = sesion_repository.get_by_id(db, sesion_id)
        if not sesion:
            raise HTTPException(status_code=404, detail="Sesión no encontrada.")
        if sesion.estado != "Programada":
            raise HTTPException(
                status_code=409,
                detail="La sesión no está disponible para reservas.",
            )

        if reserva_repository.existe_reserva_activa(db, cliente_id, sesion_id):
            raise HTTPException(
                status_code=409,
                detail="Ya tienes una reserva activa para esta sesión.",
            )

        if sesion.cupos_disponibles <= 0:
            raise HTTPException(
                status_code=409,
                detail="La sesión ha alcanzado su cupo máximo.",
            )

        if reserva_repository.hay_solapamiento(db, cliente_id, sesion):
            raise HTTPException(
                status_code=409,
                detail="Ya tienes una reserva activa en ese bloque horario.",
            )

        return reserva_repository.crear(db, cliente_id, sesion_id)

    def cancelar(self, db: Session, reserva_id: int) -> Reserva:
        reserva = self.obtener(db, reserva_id)
        if reserva.estado == "Cancelada":
            raise HTTPException(status_code=409, detail="La reserva ya fue cancelada.")
        resultado = reserva_repository.cancelar(db, reserva_id)
        if not resultado:
            raise HTTPException(status_code=500, detail="Error al cancelar la reserva.")
        return resultado


reserva_service = ReservaService()
