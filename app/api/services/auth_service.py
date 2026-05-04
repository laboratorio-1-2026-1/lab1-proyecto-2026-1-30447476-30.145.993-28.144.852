from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.rol_repository import RolRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.usuario import UsuarioCreate, LoginRequest
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta

class AuthService:
    def __init__(self, db: Session):
        self.usuario_repo = UsuarioRepository(db)
        self.rol_repo = RolRepository(db)
        self.db = db
    
    def registrar_usuario(self, usuario_create: UsuarioCreate) -> dict:
        """Registrar nuevo usuario"""
        # Verificar que el email no exista
        if self.usuario_repo.get_by_email(usuario_create.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado"
            )
        
        # Hashear contraseña
        usuario_create.contraseña = hash_password(usuario_create.contraseña)
        
        # Crear usuario
        usuario = self.usuario_repo.create(usuario_create)
        
        return {"id": usuario.id, "email": usuario.email, "rol_id": usuario.rol_id}
    
    def login(self, login_request: LoginRequest) -> dict:
        """Autenticar usuario y retornar token"""
        # Buscar usuario por email
        usuario = self.usuario_repo.get_by_email(login_request.email)
        
        if not usuario or not verify_password(
            login_request.contraseña,
            usuario.contraseña_hasheada
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        
        # Crear token
        access_token = create_access_token(
            data={
                "sub": usuario.id,
                "email": usuario.email,
                "rol": usuario.rol.nombre
            }
        )
        
        return {
            "token": access_token,
            "usuario": {
                "id": usuario.id,
                "email": usuario.email,
                "nombre": usuario.nombre,
                "rol": usuario.rol.nombre
            }
        }