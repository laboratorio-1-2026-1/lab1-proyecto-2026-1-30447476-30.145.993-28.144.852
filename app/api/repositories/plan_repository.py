        return db.query(Evaluacion).filter(Evaluacion.cliente_id == cliente_id).order_by(Evaluacion.fecha.desc()).all()  from sqlalchemy.orm import Session 
from app.api.models.plan import Plan 
 
class PlanRepository: 
    @staticmethod 
    def get_by_id(db: Session, plan_id: int) -
