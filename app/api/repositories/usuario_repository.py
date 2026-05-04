from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository
from typing import Optional

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, db: Session):
        super().__init__(Usuario, db)
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[Usuario]:
        """Obtener usuario por username"""
        return self.db.query(Usuario).filter(Usuario.nombreUsuario == username).first()