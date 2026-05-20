from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.pago import Pago
from app.api.schemas.pago import PagoCreate


class PagoRepository:
    @staticmethod
    def get_all(db: Session) -> List[Pago]:
        return db.query(Pago).order_by(Pago.fecha_pago.desc()).all()

    @staticmethod
    def get_by_id(db: Session, pago_id: int) -> Optional[Pago]:
        return db.query(Pago).filter(Pago.id == pago_id).first()

    @staticmethod
    def get_by_cliente(db: Session, cliente_id: int) -> List[Pago]:
        return db.query(Pago).filter(Pago.cliente_id == cliente_id).order_by(Pago.fecha_pago.desc()).all()

    @staticmethod
    def create(db: Session, data: PagoCreate) -> Pago:
        pago = Pago(
            cliente_id=data.cliente_id,
            plan_id=data.plan_id,
            monto=data.monto,
            fecha_pago=data.fecha_pago,
            fecha_vencimiento=data.fecha_vencimiento,
        )
        db.add(pago)
        db.commit()
        db.refresh(pago)
        return pago

    @staticmethod
    def get_ultimo_pago(db: Session, cliente_id: int) -> Optional[Pago]:
        return (
            db.query(Pago)
            .filter(Pago.cliente_id == cliente_id)
            .order_by(Pago.fecha_pago.desc())
            .first()
        )

    @staticmethod
    def membresia_activa(db: Session, cliente_id: int) -> bool:
        ultimo = PagoRepository.get_ultimo_pago(db, cliente_id)
        if not ultimo:
            return False
        return ultimo.fecha_vencimiento >= datetime.now()
