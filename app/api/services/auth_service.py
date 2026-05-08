from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.models import Usuario, Rol, UsuarioRol
from app.schemas.schemas import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:

    @staticmethod
    def register(db: Session, data: RegisterRequest) -> Usuario:
        if db.query(Usuario).filter(Usuario.email == data.email).first():
            raise HTTPException(status_code=409, detail="El email ya está registrado")
        if db.query(Usuario).filter(Usuario.nombreUsuario == data.nombreUsuario).first():
            raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")

        user = Usuario(
            nombreUsuario=data.nombreUsuario,
            email=data.email,
            password_hash=hash_password(data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, data: LoginRequest) -> dict:
        user = db.query(Usuario).filter(Usuario.email == data.email).first()
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        if not user.activo:
            raise HTTPException(status_code=403, detail="Usuario inactivo")

        token = create_access_token({"sub": str(user.idUsuarios)})
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    def assign_role(db: Session, user_id: int, rol_id: int) -> None:
        user = db.query(Usuario).filter(Usuario.idUsuarios == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        rol = db.query(Rol).filter(Rol.idRol == rol_id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        existing = db.query(UsuarioRol).filter_by(usuario_id=user_id, rol_id=rol_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="El usuario ya tiene este rol")

        db.add(UsuarioRol(usuario_id=user_id, rol_id=rol_id))
        db.commit()