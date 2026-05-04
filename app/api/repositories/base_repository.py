from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, List, Optional

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def create(self, obj_in: dict) -> ModelType:
        """Crear registro"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def read_by_id(self, id: int) -> Optional[ModelType]:
        """Obtener por ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def read_all(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        """Obtener todos con paginación"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        """Actualizar registro"""
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """Eliminar registro"""
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True