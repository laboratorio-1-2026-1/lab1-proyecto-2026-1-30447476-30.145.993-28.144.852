from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.evaluacion_biometrica import EvaluacionBiometrica

class EvaluacionRepository:

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        entrenador_id: Optional[int] = None
    ) -> List[EvaluacionBiometrica]:
        query = db.query(EvaluacionBiometrica)
        if cliente_id:
            query = query.filter(EvaluacionBiometrica.cliente_id == cliente_id)
        if entrenador_id:
            query = query.filter(EvaluacionBiometrica.entrenador_id == entrenador_id)
        return query.order_by(EvaluacionBiometrica.fechaEvaluacion.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, evaluacion_id: int) -> Optional[EvaluacionBiometrica]:
        return db.query(EvaluacionBiometrica).filter(
            EvaluacionBiometrica.idEvaluacionesBiometricas == evaluacion_id
        ).first()

    @staticmethod
    def create(db: Session, **data) -> EvaluacionBiometrica:
        evaluacion = EvaluacionBiometrica(**data)
        db.add(evaluacion)
        db.commit()
        db.refresh(evaluacion)
        return evaluacion

    @staticmethod
    def update(db: Session, evaluacion_id: int, **data) -> Optional[EvaluacionBiometrica]:
        evaluacion = EvaluacionRepository.get_by_id(db, evaluacion_id)
        if not evaluacion:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(evaluacion, key, value)
        db.commit()
        db.refresh(evaluacion)
        return evaluacion

    @staticmethod
    def delete(db: Session, evaluacion_id: int) -> bool:
        evaluacion = EvaluacionRepository.get_by_id(db, evaluacion_id)
        if not evaluacion:
            return False
        db.delete(evaluacion)
        db.commit()
        return True