from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.api.database.session import get_db
from app.api.core.security import require_roles, get_current_user
from app.api.services.usuario_service import UsuarioService
from app.api.schemas.usuario import UsuarioCreate, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
AdminOnly = require_roles("Administrador")


@router.get("", summary="Listar usuarios")
async def listar(_: dict = Depends(AdminOnly),
                 skip: int = Query(0, ge=0),
                 limit: int = Query(100, ge=1, le=500),
                 activo: Optional[bool] = Query(None),
                 rol_id: Optional[int] = Query(None),
                 db: Session = Depends(get_db)):
    return UsuarioService(db).listar_usuarios(
        skip=skip, limit=limit, activo=activo, rol_id=rol_id)


@router.get("/roles", summary="Listar roles")
async def roles(_: dict = Depends(AdminOnly),
                db: Session = Depends(get_db)):
    return UsuarioService(db).listar_roles()


@router.get("/{usuario_id}", summary="Obtener usuario")
async def obtener(usuario_id: int, _: dict = Depends(AdminOnly),
                  db: Session = Depends(get_db)):
    return UsuarioService(db).obtener_usuario(usuario_id)


@router.post("", status_code=status.HTTP_201_CREATED,
             summary="Crear usuario")
async def crear(data: UsuarioCreate, _: dict = Depends(AdminOnly),
                db: Session = Depends(get_db)):
    return UsuarioService(db).crear_usuario(data)


@router.put("/{usuario_id}", summary="Actualizar usuario")
async def actualizar(usuario_id: int, data: UsuarioUpdate,
                     cu: dict = Depends(AdminOnly),
                     db: Session = Depends(get_db)):
    return UsuarioService(db).actualizar_usuario(
        usuario_id, data, cu["user_id"])


@router.delete("/{usuario_id}", summary="Desactivar usuario")
async def desactivar(usuario_id: int, cu: dict = Depends(AdminOnly),
                     db: Session = Depends(get_db)):
    return UsuarioService(db).desactivar_usuario(
        usuario_id, cu["user_id"])


@router.patch("/{usuario_id}/activar", summary="Reactivar usuario")
async def activar(usuario_id: int, _: dict = Depends(AdminOnly),
                  db: Session = Depends(get_db)):
    return UsuarioService(db).activar_usuario(usuario_id)