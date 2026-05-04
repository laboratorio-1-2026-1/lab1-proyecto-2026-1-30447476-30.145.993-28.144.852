# app/services/usuario_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_usuario_by_email(db: Session, email: str):
    """Obtiene un usuario por su email (único)."""
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuario_by_cedula(db: Session, cedula: str):
    """Obtiene un usuario por su cédula (única)."""
    return db.query(Usuario).filter(Usuario.cedula == cedula).first()

def get_usuario_by_id(db: Session, usuario_id: int):
    """Obtiene un usuario por ID, lanza 404 si no existe."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Lista usuarios con paginación."""
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario_data: UsuarioCreate):
    """
    Crea un nuevo usuario.
    Valida que email y cédula no existan, asigna rol por defecto 'cliente' si no se especifica.
    """
    # Verificar si ya existe un usuario con el mismo email
    if get_usuario_by_email(db, usuario_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    # Verificar si ya existe un usuario con la misma cédula
    if get_usuario_by_cedula(db, usuario_data.cedula):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cédula ya está registrada"
        )
    
    # Obtener el rol (por defecto "cliente")
    rol_nombre = usuario_data.rol_nombre or "cliente"
    rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
    if not rol:
        # Si el rol no existe, crearlo? Mejor lanzar error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El rol '{rol_nombre}' no existe"
        )
    
    # Crear el usuario
    hashed = hash_password(usuario_data.password)
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        apellido=usuario_data.apellido,
        email=usuario_data.email,
        cedula=usuario_data.cedula,
        password_hash=hashed,
        rol_id=rol.id,
        activo=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    """Actualiza un usuario existente (solo campos permitidos)."""
    usuario = get_usuario_by_id(db, usuario_id)
    update_dict = usuario_data.dict(exclude_unset=True)
    
    # Si se actualiza la contraseña, hashearla
    if "password" in update_dict and update_dict["password"] is not None:
        update_dict["password_hash"] = hash_password(update_dict.pop("password"))
    
    # Si se actualiza el rol, obtener el ID del rol
    if "rol_nombre" in update_dict and update_dict["rol_nombre"] is not None:
        rol = db.query(Rol).filter(Rol.nombre == update_dict["rol_nombre"]).first()
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El rol '{update_dict['rol_nombre']}' no existe"
            )
        update_dict["rol_id"] = rol.id
        del update_dict["rol_nombre"]
    
    # Aplicar cambios
    for field, value in update_dict.items():
        setattr(usuario, field, value)
    
    db.commit()
    db.refresh(usuario)
    return usuario

def delete_usuario(db: Session, usuario_id: int):
    """Elimina físicamente un usuario (o lógicamente si se prefiere)."""
    usuario = get_usuario_by_id(db, usuario_id)
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}

def soft_delete_usuario(db: Session, usuario_id: int):
    """Desactiva un usuario (borrado lógico) manteniendo el registro."""
    usuario = get_usuario_by_id(db, usuario_id)
    usuario.activo = False
    db.commit()
    db.refresh(usuario)
    return usuario

def authenticate_usuario(db: Session, email: str, password: str):
    """
    Autentica un usuario por email y contraseña.
    Retorna el usuario si las credenciales son correctas, None si no.
    """
    usuario = get_usuario_by_email(db, email)
    if not usuario:
        return None
    if not verify_password(password, usuario.password_hash):
        return None
    if not usuario.activo:
        return None
    return usuario