        return acceso  from sqlalchemy.orm import Session 
from app.api.models.acceso import Acceso 
from datetime import datetime 
 
class AccesoRepository: 
    @staticmethod 
    def create(db: Session, cliente_id: int) -
        acceso = Acceso(cliente_id=cliente_id, fecha_hora_entrada=datetime.now()) 
        db.add(acceso) 
        db.commit() 
        db.refresh(acceso) 
