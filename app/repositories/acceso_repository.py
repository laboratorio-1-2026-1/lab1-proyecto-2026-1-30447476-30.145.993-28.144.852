from app.models.acceso import Acceso 
from app.repositories.base_repository import BaseRepository 
from datetime import datetime 
 
class AccesoRepository(BaseRepository): 
    def __init__(self): 
        super().__init__(Acceso) 
 
    def registrar_entrada(self, cliente_id): 
        return self.create(cliente_id=cliente_id, fecha_hora_entrada=datetime.now()) 
