from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.session import get_db
from app.core.security import require_role, get_current_user
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.core.security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=dict)
async def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    email: Optional[str] = None,
    rol_id: Optional[int] = None,
    activo: Optional[bool] = None,
    current_user = Depends(require_role("ADMINISTRADOR")),
    db: Session = Depends(get_db)
):
    """
    Listar todos los usuarios con filtros opcionales.
    **Solo ADMINISTRADOR**
    """
    repo = UsuarioRepository(db)
    
    # Construir filtros dinámicamente
    filters = {}
    if email:
        filters["email"] = email
    if rol_id:
        filters["rol_id"] = rol_id
    if activo is not None:
        filters["activo"] = activo
    
    usuarios = repo.read_all(skip=skip, limit=limit, filters=filters)
    
    # Convertir a respuesta (ocultar password_hash)
    data = []
    for u in usuarios:
        data.append({
            "idUsuarios": u.idUsuarios,
            "nombreUsuario": u.nombreUsuario,
            "email": u.email,
            "rol_id": u.rol_id,
            "activo": u.activo,
            "created_at": u.created_at
        })
    
    return {
        "status": "success",
        "data": data,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": len(data)
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/{usuario_id}", response_model=dict)
async def obtener_usuario(
    usuario_id: int,
    current_user = Depends(require_role("ADMINISTRADOR")),
    db: Session = Depends(get_db)
):
    """
    Obtener un usuario por su ID.
    **Solo ADMINISTRADOR**
    """
    repo = UsuarioRepository(db)
    usuario = repo.read_by_id(usuario_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Not Found",
                "codigoInterno": "ERR_USUARIO_NO_ENCONTRADO",
                "mensaje": f"Usuario con ID {usuario_id} no encontrado"
            }
        )
    
    return {
        "status": "success",
        "data": {
            "idUsuarios": usuario.idUsuarios,
            "nombreUsuario": usuario.nombreUsuario,
            "email": usuario.email,
            "rol_id": usuario.rol_id,
            "activo": usuario.activo,
            "created_at": usuario.created_at
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_usuario(
    usuario_create: UsuarioCreate,
    current_user = Depends(require_role("ADMINISTRADOR")),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo usuario (empleados, entrenadores, etc.).
    **Solo ADMINISTRADOR**
    """
    repo = UsuarioRepository(db)
    
    # Verificar email duplicado
    existing = repo.get_by_email(usuario_create.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Conflict",
                "codigoInterno": "ERR_EMAIL_DUPLICADO",
                "mensaje": f"El email {usuario_create.email} ya está registrado"
            }
        )
    
    # Verificar nombre de usuario duplicado
    existing_username = repo.get_by_username(usuario_create.nombreUsuario)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Conflict",
                "codigoInterno": "ERR_USERNAME_DUPLICADO",
                "mensaje": f"El nombre de usuario {usuario_create.nombreUsuario} ya está en uso"
            }
        )
    
    # Crear usuario
    password_hashed = hash_password(usuario_create.password)
    nuevo_usuario = repo.create({
        "nombreUsuario": usuario_create.nombreUsuario,
        "email": usuario_create.email,
        "password_hash": password_hashed,
        "rol_id": usuario_create.rol_id,
        "activo": True
    })
    
    return {
        "status": "success",
        "mensaje": "Usuario creado exitosamente",
        "data": {
            "idUsuarios": nuevo_usuario.idUsuarios,
            "nombreUsuario": nuevo_usuario.nombreUsuario,
            "email": nuevo_usuario.email,
            "rol_id": nuevo_usuario.rol_id,
            "activo": nuevo_usuario.activo
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.put("/{usuario_id}", response_model=dict)
async def actualizar_usuario(
    usuario_id: int,
    usuario_update: dict,  # Puedes crear un schema UsuarioUpdate si lo prefieres
    current_user = Depends(require_role("ADMINISTRADOR")),
    db: Session = Depends(get_db)
):
    """
    Actualizar datos de un usuario.
    **Solo ADMINISTRADOR**
    """
    repo = UsuarioRepository(db)
    
    # Verificar que existe
    usuario = repo.read_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Not Found",
                "codigoInterno": "ERR_USUARIO_NO_ENCONTRADO",
                "mensaje": f"Usuario con ID {usuario_id} no encontrado"
            }
        )
    
    # Si se actualiza email, verificar no duplicado
    if "email" in usuario_update:
        existing = repo.get_by_email(usuario_update["email"])
        if existing and existing.idUsuarios != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_EMAIL_DUPLICADO",
                    "mensaje": f"El email {usuario_update['email']} ya está en uso"
                }
            )
    
    # Si se actualiza password, hashearlo
    if "password" in usuario_update:
        usuario_update["password_hash"] = hash_password(usuario_update.pop("password"))
    
    # Actualizar
    usuario_actualizado = repo.update(usuario_id, usuario_update)
    
    return {
        "status": "success",
        "mensaje": "Usuario actualizado exitosamente",
        "data": {
            "idUsuarios": usuario_actualizado.idUsuarios,
            "nombreUsuario": usuario_actualizado.nombreUsuario,
            "email": usuario_actualizado.email,
            "rol_id": usuario_actualizado.rol_id,
            "activo": usuario_actualizado.activo
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK, response_model=dict)
async def eliminar_usuario(
    usuario_id: int,
    current_user = Depends(require_role("ADMINISTRADOR")),
    db: Session = Depends(get_db)
):
    """
    Eliminar (desactivar) un usuario.
    **Solo ADMINISTRADOR**
    """
    repo = UsuarioRepository(db)
    
    # Verificar que existe
    usuario = repo.read_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Not Found",
                "codigoInterno": "ERR_USUARIO_NO_ENCONTRADO",
                "mensaje": f"Usuario con ID {usuario_id} no encontrado"
            }
        )
    
    # No permitir eliminar al propio admin
    if usuario_id == current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Bad Request",
                "codigoInterno": "ERR_NO_SELF_DELETE",
                "mensaje": "No puedes eliminar tu propio usuario"
            }
        )
    
    # Desactivar lógicamente (soft delete)
    repo.update(usuario_id, {"activo": False})
    
    return {
        "status": "success",
        "mensaje": f"Usuario {usuario.nombreUsuario} desactivado exitosamente",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.patch("/{usuario_id}/activar", response_model=dict)
async def activar_usuario(
    usuario_id: int,
    current_user = Depends(require_role("ADMINISTRADOR")),
    db: Session = Depends(get_db)
):
    """
    Reactivar un usuario desactivado.
    **Solo ADMINISTRADOR**
    """
    repo = UsuarioRepository(db)
    
    usuario = repo.read_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Not Found",
                "codigoInterno": "ERR_USUARIO_NO_ENCONTRADO",
                "mensaje": f"Usuario con ID {usuario_id} no encontrado"
            }
        )
    
    repo.update(usuario_id, {"activo": True})
    
    return {
        "status": "success",
        "mensaje": f"Usuario {usuario.nombreUsuario} activado exitosamente",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/me/reservas", response_model=dict)
async def mis_reservas(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener las reservas del usuario autenticado.
    Para clientes: ver sus propias reservas.
    """
    from app.repositories.reserva_repository import ReservaRepository
    from app.models.cliente import Cliente
    
    # Obtener el cliente asociado al usuario
    cliente_repo = ClienteRepository(db)  # Necesitarías crear este repo
    cliente = db.query(Cliente).filter(Cliente.usuario_id == current_user["user_id"]).first()
    
    if not cliente:
        return {
            "status": "success",
            "data": [],
            "mensaje": "No eres un cliente registrado",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    reserva_repo = ReservaRepository(db)
    reservas = reserva_repo.get_by_cliente_id(cliente.idClientes)
    
    return {
        "status": "success",
        "data": reservas,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }