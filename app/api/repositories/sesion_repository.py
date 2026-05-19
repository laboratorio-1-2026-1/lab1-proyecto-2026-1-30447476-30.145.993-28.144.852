from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models.sesion import Sesion


class SesionRepository:
    @staticmethod
    def get_by_id(db: Session, sesion_id: int) -> Optional[Sesion]:
        return db.query(Sesion).filter(Sesion.id == sesion_id).first()

    @staticmethod
    def get_by_fecha(db: Session, fecha: date) -> List[Sesion]:
        return db.query(Sesion).filter(Sesion.fecha == fecha).all()

    @staticmethod
    def update_cupos(db: Session, sesion_id: int, nuevos_cupos: int) -> Optional[Sesion]:
        sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
        if sesion:
            sesion.cupos_disponibles = nuevos_cupos
            db.commit()
            db.refresh(sesion)
        return sesion


sesion_repository = SesionRepository()
