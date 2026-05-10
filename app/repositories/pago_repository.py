from app.models.pago import Pago 
from app.repositories.base_repository import BaseRepository 
from datetime import datetime 
 
class PagoRepository(BaseRepository): 
    def __init__(self): 
        super().__init__(Pago) 
 
    def get_ultimo_pago(self, cliente_id): 
        db = self._get_db() 
        try: 
            return db.query(Pago).filter(Pago.cliente_id == cliente_id).order_by(Pago.fecha_pago.desc()).first() 
        finally: 
            db.close() 
 
    def membresia_activa(self, cliente_id): 
        ultimo = self.get_ultimo_pago(cliente_id) 
        if not ultimo: 
            return False 
        return ultimo.fecha_vencimiento 
