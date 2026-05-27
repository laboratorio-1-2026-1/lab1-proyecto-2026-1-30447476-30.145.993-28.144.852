from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.cliente import Cliente

class ClienteRepository:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
        return db.query(Cliente).order_by(Cliente.idCliente).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, cliente_id: int) -> Optional[Cliente]:
        return db.query(Cliente).filter(Cliente.idCliente == cliente_id).first()

    @staticmethod
    def get_by_cedula(db: Session, cedula: str) -> Optional[Cliente]:
        return db.query(Cliente).filter(Cliente.cedula == cedula).first()

    @staticmethod
    def create(db: Session, **data) -> Cliente:
        cliente = Cliente(**data)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def update(db: Session, cliente_id: int, **data) -> Optional[Cliente]:
        cliente = ClienteRepository.get_by_id(db, cliente_id)
        if not cliente:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(cliente, key, value)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def delete(db: Session, cliente_id: int) -> bool:
        cliente = ClienteRepository.get_by_id(db, cliente_id)
        if not cliente:
            return False
        db.delete(cliente)
        db.commit()
        return True