from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, List, Optional, Any, Dict

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Repositorio base con operaciones CRUD genéricas"""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """Obtiene todos los registros con paginación y filtros opcionales"""
        query = self.db.query(self.model)
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.filter(getattr(self.model, field) == value)
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Obtiene un registro por su ID (detecta automáticamente el nombre de la PK)"""
        pk_col = self.model.__table__.primary_key.columns.values()[0].name
        return self.db.query(self.model).filter(
            getattr(self.model, pk_col) == id
        ).first()

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Crea un nuevo registro"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Actualiza un registro existente"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Elimina un registro físicamente"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        self.db.delete(db_obj)
        self.db.flush()
        return True

    def soft_delete(self, id: int) -> Optional[ModelType]:
        """Eliminación lógica (requiere campo 'activo' en el modelo)"""
        return self.update(id, {"activo": False})