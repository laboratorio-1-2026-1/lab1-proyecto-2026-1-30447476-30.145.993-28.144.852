        return acceso  from sqlalchemy.orm import Session 
from app.api.models.pago import Pago 
from datetime import datetime 
 
class PagoRepository: 
    @staticmethod 
    def get_ultimo_pago(db: Session, cliente_id: int) -
        return db.query(Pago).filter(Pago.cliente_id == cliente_id).order_by(Pago.fecha_pago.desc()).first() 
 
    @staticmethod 
    def membresia_activa(db: Session, cliente_id: int) -
        ultimo = PagoRepository.get_ultimo_pago(db, cliente_id) 
        if not ultimo: return False 
