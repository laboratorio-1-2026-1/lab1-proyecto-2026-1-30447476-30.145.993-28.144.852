from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import SesionProgramada
from app.repositories.base_repository import BaseRepository


class SesionRepository(BaseRepository[SesionProgramada]):

    def __init__(self):
        super().__init__(SesionProgramada)

    def get_todas(
        self,
        db: Session,
        fecha: Optional[date] = None,
        disciplina_id: Optional[int] = None,
        entrenador_id: Optional[int] = None,
    ) -> List[SesionProgramada]:
        q = db.query(SesionProgramada)
        if fecha:
            q = q.filter(SesionProgramada.fechaHoraInicio >= str(fecha))
        if disciplina_id:
            q = q.filter(SesionProgramada.disciplina_id == disciplina_id)
        if entrenador_id:
            q = q.filter(SesionProgramada.entrenador_id == entrenador_id)
        return q.order_by(SesionProgramada.fechaHoraInicio).all()

    def get_disponibles(self, db: Session) -> List[SesionProgramada]:
        """Sesiones programadas con cupos > 0."""
        return (
            db.query(SesionProgramada)
            .filter(
                SesionProgramada.estado == "Programada",
                SesionProgramada.cuposDisponibles > 0,
            )
            .order_by(SesionProgramada.fechaHoraInicio)
            .all()
        )

    def crear(self, db: Session, datos: dict) -> SesionProgramada:
        sesion = SesionProgramada(
            **datos,
            cuposDisponibles=datos["cupoMaximo"],  # al crear, cupos disponibles = máximo
        )
        db.add(sesion)
        db.commit()
        db.refresh(sesion)
        return sesion

    def cancelar(self, db: Session, sesion_id: int) -> Optional[SesionProgramada]:
        sesion = self.get_by_id(db, sesion_id)
        if not sesion:
            return None
        sesion.estado = "Cancelada"
        db.commit()
        db.refresh(sesion)
        return sesion


sesion_repository = SesionRepository()