        return db.query(Usuario).filter(Usuario.cedula == cedula).first()  from sqlalchemy.orm import Session 
from app.api.models.usuario import Usuario 
 
class UsuarioRepository: 
    @staticmethod 
    def get_by_cedula(db: Session, cedula: str) -
