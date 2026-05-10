from app.models.evaluacion import Evaluacion 
from app.repositories.base_repository import BaseRepository 
 
class EvaluacionRepository(BaseRepository): 
    def __init__(self): 
        super().__init__(Evaluacion) 
 
    def get_by_cliente(self, cliente_id): 
        db = self._get_db() 
        try: 
            return db.query(Evaluacion).filter(Evaluacion.cliente_id == cliente_id).order_by(Evaluacion.fecha.desc()).all() 
        finally: 
            db.close() 
