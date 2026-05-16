from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.api.repositories.usuario_repository import UsuarioRepository, RolRepository
from app.api.core.security import hash_password, verify_password, create_access_token
from app.api.schemas.usuario import RegisterRequest, LoginRequest
from app.api.exceptions.custom_exceptions import (
    conflict_response, unauthorized_response, not_found_response,
)


def _ts():
    return datetime.now(timezone.utc).isoformat() + "Z"


class AuthService:
    def __init__(self, db: Session):
        self.usuarios = UsuarioRepository(db)
        self.roles    = RolRepository(db)

    def registrar_usuario(self, data: RegisterRequest) -> dict:
        if self.usuarios.get_by_email(data.email):
            conflict_response("ERR_EMAIL_DUPLICADO",
                              f"El email '{data.email}' ya está registrado.")
        if self.usuarios.get_by_username(data.nombreUsuario):
            conflict_response("ERR_USERNAME_DUPLICADO",
                              f"El usuario '{data.nombreUsuario}' ya existe.")
        rol = self.roles.get_by_id(data.rol_id)
        if not rol:
            not_found_response("ERR_ROL_NO_ENCONTRADO",
                               f"Rol con ID {data.rol_id} no existe.")
        nuevo = self.usuarios.create(
            nombreUsuario = data.nombreUsuario,
            email         = data.email,
            password_hash = hash_password(data.password),
            rol_id        = data.rol_id,
        )
        return {
            "status":  "success",
            "mensaje": "Usuario registrado exitosamente.",
            "data": {
                "idUsuarios":    nuevo.idUsuarios,
                "nombreUsuario": nuevo.nombreUsuario,
                "email":         nuevo.email,
                "rol":           rol.nombreRol,
            },
            "timestamp": _ts(),
        }

    def login(self, data: LoginRequest) -> dict:
        usuario = self.usuarios.get_by_email(data.email)
        if not usuario or not verify_password(data.password,
                                              usuario.password_hash):
            unauthorized_response("ERR_CREDENCIALES_INVALIDAS",
                                  "Email o contraseña incorrectos.")
        if not usuario.activo:
            unauthorized_response("ERR_USUARIO_INACTIVO",
                                  "Usuario desactivado.")
        token = create_access_token({
            "sub":    str(usuario.idUsuarios),
            "email":  usuario.email,
            "rol":    usuario.rol.nombreRol,
            "activo": usuario.activo,
        })
        return {
            "status":     "success",
            "mensaje":    "Login exitoso.",
            "token":      token,
            "token_type": "bearer",
            "data": {
                "idUsuarios":    usuario.idUsuarios,
                "nombreUsuario": usuario.nombreUsuario,
                "email":         usuario.email,
                "rol":           usuario.rol.nombreRol,
            },
            "timestamp": _ts(),
        }

    def get_perfil(self, user_id: int) -> dict:
        u = self.usuarios.get_by_id(user_id)
        if not u:
            not_found_response("ERR_USUARIO_NO_ENCONTRADO",
                               f"Usuario ID {user_id} no encontrado.")
        return {
            "status": "success",
            "data": {
                "idUsuarios":    u.idUsuarios,
                "nombreUsuario": u.nombreUsuario,
                "email":         u.email,
                "rol":           u.rol.nombreRol,
                "activo":        u.activo,
                "created_at":    u.created_at.isoformat(),
            },
            "timestamp": _ts(),
        }