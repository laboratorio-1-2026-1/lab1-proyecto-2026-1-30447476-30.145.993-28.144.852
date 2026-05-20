from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.evaluacion import Evaluacion
from app.api.schemas.evaluacion import EvaluacionCreate


class EvaluacionRepository:
    @staticmethod
    def get_all(db: Session) -> List[Evaluacion]:
        return db.query(Evaluacion).order_by(Evaluacion.fecha.desc()).all()

    @staticmethod
    def get_by_id(db: Session, evaluacion_id: int) -> Optional[Evaluacion]:
        return db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()

    @staticmethod
    def get_by_cliente(db: Session, cliente_id: int) -> List[Evaluacion]:
        return (
            db.query(Evaluacion)
            .filter(Evaluacion.cliente_id == cliente_id)
            .order_by(Evaluacion.fecha.desc())
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        cliente_id: int,
        entrenador_id: int,
        peso: float,
        estatura: float,
        grasa_corporal: Optional[float],
        observaciones: Optional[str],
        fecha: datetime,
    ) -> Evaluacion:
        evaluacion = Evaluacion(
            cliente_id=cliente_id,
            entrenador_id=entrenador_id,
            peso=peso,
            estatura=estatura,
            grasa_corporal=grasa_corporal,
            observaciones=observaciones,
            fecha=fecha,
        )
        db.add(evaluacion)
        db.commit()
        db.refresh(evaluacion)
        return evaluacion
