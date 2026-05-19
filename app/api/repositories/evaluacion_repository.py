        return ultimo.fecha_vencimiento  from sqlalchemy.orm import Session 
from app.api.models.evaluacion import Evaluacion 
from datetime import datetime 
 
class EvaluacionRepository: 
    @staticmethod 
    def get_by_cliente(db: Session, cliente_id: int) -
