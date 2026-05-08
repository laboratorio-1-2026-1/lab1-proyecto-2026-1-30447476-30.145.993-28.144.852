from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Reserva, SesionProgramada, Cliente
from app.repositories.reserva_repository import reserva_repository
from app.repositories.cliente_repository import cliente_repository
from app.repositories.sesion_repository import sesion_repository


class ReservaService:

    def listar_todas(self, db: Session) -> List[Reserva]:
        return (
            db.query(Reserva)
            .order_by(Reserva.fechaReservacion.desc())
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
        # 1. Verificar que el cliente existe
        cliente = cliente_repository.get_by_id(db, cliente_id)
        if not cliente or not cliente.activo:
            raise HTTPException(status_code=404, detail="Cliente no encontrado o inactivo.")

        # 2. Verificar que la sesión existe y está programada
        sesion = sesion_repository.get_by_id(db, sesion_id)
        if not sesion:
            raise HTTPException(status_code=404, detail="Sesión no encontrada.")
        if sesion.estado != "Programada":
            raise HTTPException(
                status_code=409,
                detail="La sesión no está disponible para reservas."
            )

        # 3. Regla de negocio: verificar reserva duplicada
        if reserva_repository.existe_reserva_activa(db, cliente_id, sesion_id):
            raise HTTPException(
                status_code=409,
                detail="Ya tienes una reserva activa para esta sesión."
            )

        # 4. Regla de negocio crítica: cupos disponibles
        if sesion.cuposDisponibles <= 0:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"La sesión ha alcanzado su cupo máximo "
                    f"(cuposDisponibles: 0)."
                ),
            )

        # 5. Regla de negocio crítica: solapamiento de horarios
        if reserva_repository.hay_solapamiento(db, cliente_id, sesion):
            raise HTTPException(
                status_code=409,
                detail="Ya tienes una reserva activa en ese bloque horario.",
            )

        return reserva_repository.crear(db, cliente_id, sesion_id)

    def cancelar(self, db: Session, reserva_id: int, usuario_actual) -> Reserva:
        reserva = self.obtener(db, reserva_id)

        if reserva.estado == "Cancelada":
            raise HTTPException(status_code=409, detail="La reserva ya fue cancelada.")

        # Solo el propietario o un Admin puede cancelar
        roles = [ur.rol.nombreRol for ur in usuario_actual.roles]
        es_admin = "Administrador" in roles
        es_propietario = (
            usuario_actual.cliente
            and usuario_actual.cliente.idClientes == reserva.cliente_id
        )
        if not es_admin and not es_propietario:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para cancelar esta reserva."
            )

        resultado = reserva_repository.cancelar(db, reserva_id)
        if not resultado:
            raise HTTPException(status_code=500, detail="Error al cancelar la reserva.")
        return resultado


reserva_service = ReservaService()