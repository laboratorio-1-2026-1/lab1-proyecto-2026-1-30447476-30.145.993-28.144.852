from app.models.reserva import Reserva 
from app.repositories.base_repository import BaseRepository 
 
class ReservaRepository(BaseRepository): 
    def __init__(self): 
        super().__init__(Reserva) 
 
    def get_by_cliente(self, cliente_id): 
        db = self._get_db() 
        try: 
            return db.query(Reserva).filter(Reserva.cliente_id == cliente_id).all() 
        finally: 
            db.close() 
