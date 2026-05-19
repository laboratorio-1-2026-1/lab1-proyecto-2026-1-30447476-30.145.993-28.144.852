from sqlalchemy.orm import Session 
from typing import List, Optional, Type, TypeVar 
 
ModelType = TypeVar("ModelType") 
 
class BaseRepository: 
    @staticmethod 
    def create(db: Session, model: Type[ModelType], **kwargs) -
        instance = model(**kwargs) 
        db.add(instance) 
        db.commit() 
        db.refresh(instance) 
        return instance 
 
    @staticmethod 
    def get_by_id(db: Session, model: Type[ModelType], id: int) -
        return db.query(model).filter(model.id == id).first() 
 
    @staticmethod 
    def delete(db: Session, instance) -
        db.delete(instance) 
