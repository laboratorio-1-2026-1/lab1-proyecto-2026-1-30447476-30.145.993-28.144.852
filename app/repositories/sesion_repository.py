from app.models.sesion import Sesion 
from app.repositories.base_repository import BaseRepository 
 
class SesionRepository(BaseRepository): 
    def __init__(self): 
        super().__init__(Sesion) 
 
    def get_by_fecha(self, fecha): 
        db = self._get_db() 
        try: 
            return db.query(Sesion).filter(Sesion.fecha == fecha).all() 
        finally: 
            db.close() 
