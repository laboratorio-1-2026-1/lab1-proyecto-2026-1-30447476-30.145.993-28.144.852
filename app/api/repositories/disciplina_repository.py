from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.disciplina import Disciplina

class DisciplinaRepository:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Disciplina]:
        return db.query(Disciplina).order_by(Disciplina.idDisciplina).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, disciplina_id: int) -> Optional[Disciplina]:
        return db.query(Disciplina).filter(Disciplina.idDisciplina == disciplina_id).first()

    @staticmethod
    def get_by_nombre(db: Session, nombre: str) -> Optional[Disciplina]:
        return db.query(Disciplina).filter(Disciplina.nombre == nombre).first()

    @staticmethod
    def create(db: Session, **data) -> Disciplina:
        disciplina = Disciplina(**data)
        db.add(disciplina)
        db.commit()
        db.refresh(disciplina)
        return disciplina

    @staticmethod
    def update(db: Session, disciplina_id: int, **data) -> Optional[Disciplina]:
        disciplina = DisciplinaRepository.get_by_id(db, disciplina_id)
        if not disciplina:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(disciplina, key, value)
        db.commit()
        db.refresh(disciplina)
        return disciplina

    @staticmethod
    def delete(db: Session, disciplina_id: int) -> bool:
        disciplina = DisciplinaRepository.get_by_id(db, disciplina_id)
        if not disciplina:
            return False
        db.delete(disciplina)
        db.commit()
        return True