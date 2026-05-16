from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.api.repositories.usuario_repository import UsuarioRepository, RolRepository
from app.api.core.security import hash_password
from app.api.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.api.exceptions.custom_exceptions import (
    conflict_response, not_found_response, bad_request_response,
)


def _ts():
    return datetime.now(timezone.utc).isoformat() + "Z"


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)
        self.roles = RolRepository(db)

    def listar_usuarios(self, skip=0, limit=100,
                        activo=None, rol_id=None) -> dict:
        usuarios = self.repo.get_all(skip=skip, limit=limit,
                                     activo=activo, rol_id=rol_id)
        return {
            "status": "success",
            "data": [self._fmt(u) for u in usuarios],
            "pagination": {"skip": skip, "limit": limit,
                           "total": len(usuarios)},
            "timestamp": _ts(),
        }

    def listar_roles(self) -> dict:
        roles = self.roles.get_all()
        return {
            "status": "success",
            "data": [{"idRol": r.idRol, "nombreRol": r.nombreRol,
                      "descripcion": r.descripcion} for r in roles],
            "timestamp": _ts(),
        }

    def obtener_usuario(self, usuario_id: int) -> dict:
        u = self.repo.get_by_id(usuario_id)
        if not u:
            not_found_response("ERR_USUARIO_NO_ENCONTRADO",
                               f"Usuario {usuario_id} no encontrado.")
        return {"status": "success", "data": self._fmt(u), "timestamp": _ts()}

    def crear_usuario(self, data: UsuarioCreate) -> dict:
        if self.repo.get_by_email(data.email):
            conflict_response("ERR_EMAIL_DUPLICADO",
                              f"El email '{data.email}' ya existe.")
        if self.repo.get_by_username(data.nombreUsuario):
            conflict_response("ERR_USERNAME_DUPLICADO",
                              f"El usuario '{data.nombreUsuario}' ya existe.")
        rol = self.roles.get_by_id(data.rol_id)
        if not rol:
            not_found_response("ERR_ROL_NO_ENCONTRADO",
                               f"Rol ID {data.rol_id} no existe.")
        u = self.repo.create(
            nombreUsuario = data.nombreUsuario,
            email         = data.email,
            password_hash = hash_password(data.password),
            rol_id        = data.rol_id,
        )
        return {"status": "success", "mensaje": "Usuario creado.",
                "data": self._fmt(u), "timestamp": _ts()}

    def actualizar_usuario(self, usuario_id: int,
                           data: UsuarioUpdate,
                           current_user_id: int) -> dict:
        u = self.repo.get_by_id(usuario_id)
        if not u:
            not_found_response("ERR_USUARIO_NO_ENCONTRADO",
                               f"Usuario {usuario_id} no encontrado.")
        campos = data.model_dump(exclude_none=True)
        if "email" in campos:
            ex = self.repo.get_by_email(campos["email"])
            if ex and ex.idUsuarios != usuario_id:
                conflict_response("ERR_EMAIL_DUPLICADO",
                                  f"Email '{campos['email']}' ya en uso.")
        if "nombreUsuario" in campos:
            ex = self.repo.get_by_username(campos["nombreUsuario"])
            if ex and ex.idUsuarios != usuario_id:
                conflict_response("ERR_USERNAME_DUPLICADO",
                                  f"Usuario '{campos['nombreUsuario']}' ya existe.")
        actualizado = self.repo.update(usuario_id, campos)
        return {"status": "success", "mensaje": "Usuario actualizado.",
                "data": self._fmt(actualizado), "timestamp": _ts()}

    def desactivar_usuario(self, usuario_id: int,
                           current_user_id: int) -> dict:
        if usuario_id == current_user_id:
            bad_request_response("ERR_NO_SELF_DELETE",
                                 "No puedes desactivar tu propia cuenta.")
        u = self.repo.get_by_id(usuario_id)
        if not u:
            not_found_response("ERR_USUARIO_NO_ENCONTRADO",
                               f"Usuario {usuario_id} no encontrado.")
        self.repo.desactivar(usuario_id)
        return {"status": "success",
                "mensaje": f"Usuario '{u.nombreUsuario}' desactivado.",
                "timestamp": _ts()}

    def activar_usuario(self, usuario_id: int) -> dict:
        u = self.repo.get_by_id(usuario_id)
        if not u:
            not_found_response("ERR_USUARIO_NO_ENCONTRADO",
                               f"Usuario {usuario_id} no encontrado.")
        self.repo.activar(usuario_id)
        return {"status": "success",
                "mensaje": f"Usuario '{u.nombreUsuario}' activado.",
                "timestamp": _ts()}

    def _fmt(self, u) -> dict:
        return {
            "idUsuarios":    u.idUsuarios,
            "nombreUsuario": u.nombreUsuario,
            "email":         u.email,
            "rol":           u.rol.nombreRol if u.rol else None,
            "rol_id":        u.rol_id,
            "activo":        u.activo,
            "created_at":    u.created_at.isoformat(),
        }