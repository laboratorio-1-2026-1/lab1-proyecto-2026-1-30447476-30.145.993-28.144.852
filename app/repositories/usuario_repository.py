from app.models.usuario import Usuario 
from app.repositories.base_repository import BaseRepository 
 
class UsuarioRepository(BaseRepository): 
    def __init__(self): 
        super().__init__(Usuario) 
 
    def get_by_cedula(self, cedula): 
        db = self._get_db() 
        try: 
            return db.query(Usuario).filter(Usuario.cedula == cedula).first() 
        finally: 
            db.close() 
