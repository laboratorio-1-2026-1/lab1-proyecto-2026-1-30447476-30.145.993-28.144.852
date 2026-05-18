from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.database.session import get_db
from app.api.core.security import get_current_user
from app.api.services.auth_service import AuthService
from app.api.schemas.usuario import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", status_code=status.HTTP_201_CREATED,
             summary="Registrar nuevo usuario")
async def registrar(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).registrar_usuario(data)


@router.post("/login", status_code=status.HTTP_200_OK,
             summary="Iniciar sesión — retorna Bearer Token")
async def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    return AuthService(db).login(data)


@router.get("/me", summary="Mi perfil — requiere Bearer Token")
async def mi_perfil(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AuthService(db).get_perfil(current_user["user_id"])