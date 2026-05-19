from sqlalchemy.orm import Session 
from app.api.models.reserva import Reserva 
from datetime import datetime 
 
class ReservaRepository: 
    @staticmethod 
    def create(db: Session, cliente_id: int, sesion_id: int) -
        reserva = Reserva(cliente_id=cliente_id, sesion_id=sesion_id, fecha_reserva=datetime.now()) 
        db.add(reserva) 
        db.commit() 
        db.refresh(reserva) 
