from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.auth_service import AuthService
from app.schemas.usuario import UsuarioCreate, LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def registrar(
    usuario_create: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """Registrar nuevo usuario"""
    servicio = AuthService(db)
    resultado = servicio.registrar_usuario(usuario_create)
    
    from datetime import datetime
    return {
        "status": "success",
        "mensaje": "Usuario registrado exitosamente",
        "data": resultado,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    """Iniciar sesión"""
    servicio = AuthService(db)
    return servicio.login(login_request)

@router.get("/me")
async def obtener_perfil(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener perfil del usuario autenticado"""
    from app.repositories.usuario_repository import UsuarioRepository
    repo = UsuarioRepository(db)
    usuario = repo.read_by_id(current_user["user_id"])
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    from datetime import datetime
    return {
        "status": "success",
        "data": {
            "idUsuarios": usuario.idUsuarios,
            "email": usuario.email,
            "nombreUsuario": usuario.nombreUsuario,
            "rol": usuario.rol.nombreRol
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }