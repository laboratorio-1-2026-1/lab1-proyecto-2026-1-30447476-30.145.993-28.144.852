from sqlalchemy.orm import Session
from typing import Optional, List
from app.api.models.usuario import Usuario
from app.api.models.rol import Rol


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(
            Usuario.idUsuarios == usuario_id
        ).first()

    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(
            Usuario.email == email
        ).first()

    def get_by_username(self, username: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(
            Usuario.nombreUsuario == username
        ).first()

    def get_all(self, skip=0, limit=100,
                activo=None, rol_id=None) -> List[Usuario]:
        q = self.db.query(Usuario)
        if activo is not None:
            q = q.filter(Usuario.activo == activo)
        if rol_id is not None:
            q = q.filter(Usuario.rol_id == rol_id)
        return q.offset(skip).limit(limit).all()

    def create(self, nombreUsuario: str, email: str,
               password_hash: str, rol_id: int) -> Usuario:
        u = Usuario(
            nombreUsuario = nombreUsuario,
            email         = email,
            password_hash = password_hash,
            rol_id        = rol_id,
            activo        = True,
        )
        self.db.add(u)
        self.db.flush()
        self.db.refresh(u)
        return u

    def update(self, usuario_id: int, campos: dict) -> Optional[Usuario]:
        u = self.get_by_id(usuario_id)
        if not u:
            return None
        for field, value in campos.items():
            if hasattr(u, field):
                setattr(u, field, value)
        self.db.flush()
        self.db.refresh(u)
        return u

    def desactivar(self, usuario_id: int):
        return self.update(usuario_id, {"activo": False})

    def activar(self, usuario_id: int):
        return self.update(usuario_id, {"activo": True})


class RolRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, rol_id: int) -> Optional[Rol]:
        return self.db.query(Rol).filter(Rol.idRol == rol_id).first()

    def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        return self.db.query(Rol).filter(Rol.nombreRol == nombre).first()

    def get_all(self) -> List[Rol]:
        return self.db.query(Rol).all()