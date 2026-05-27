from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.entrenador import Entrenador

class EntrenadorRepository:

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, solo_activos: bool = True) -> List[Entrenador]:
        query = db.query(Entrenador)
        if solo_activos:
            query = query.filter(Entrenador.activo == True)
        return query.order_by(Entrenador.idEntrenador).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, entrenador_id: int) -> Optional[Entrenador]:
        return db.query(Entrenador).filter(Entrenador.idEntrenador == entrenador_id).first()

    @staticmethod
    def get_by_cedula(db: Session, cedula: str) -> Optional[Entrenador]:
        return db.query(Entrenador).filter(Entrenador.cedula == cedula).first()

    @staticmethod
    def get_by_correo(db: Session, correo: str) -> Optional[Entrenador]:
        return db.query(Entrenador).filter(Entrenador.correo == correo).first()

    @staticmethod
    def get_by_usuario_id(db: Session, usuario_id: int) -> Optional[Entrenador]:
        return db.query(Entrenador).filter(Entrenador.usuario_id == usuario_id).first()

    @staticmethod
    def create(db: Session, **data) -> Entrenador:
        entrenador = Entrenador(**data)
        db.add(entrenador)
        db.commit()
        db.refresh(entrenador)
        return entrenador

    @staticmethod
    def update(db: Session, entrenador_id: int, **data) -> Optional[Entrenador]:
        entrenador = EntrenadorRepository.get_by_id(db, entrenador_id)
        if not entrenador:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(entrenador, key, value)
        db.commit()
        db.refresh(entrenador)
        return entrenador

    @staticmethod
    def delete(db: Session, entrenador_id: int) -> bool:
        entrenador = EntrenadorRepository.get_by_id(db, entrenador_id)
        if not entrenador:
            return False
        entrenador.activo = False   # borrado lógico
        db.commit()
        return True