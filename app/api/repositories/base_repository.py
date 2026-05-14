from sqlalchemy.orm import Session
from typing import TypeVar, Generic, List, Optional
from app.api.database.session import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Repositorio base con operaciones CRUD genéricas"""

    def __init__(self, model: type[ModelType]):
        self.model = model

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, data: dict) -> ModelType:
        instance = self.model(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    def update(self, db: Session, id: int, data: dict) -> Optional[ModelType]:
        instance = self.get_by_id(db, id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            db.commit()
            db.refresh(instance)
        return instance

    def delete(self, db: Session, id: int) -> bool:
        instance = self.get_by_id(db, id)
        if instance:
            db.delete(instance)
            db.commit()
            return True
        return False