from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.schemas.categoriasMaquinas import (
    CategoriaMaquinaCreate,
    CategoriaMaquinaResponse)
from app.api.repositories.maquina_repository import MaquinaRepository

router = APIRouter(prefix="/categorias-maquinas", tags=["Máquinas e Instalaciones"])


@router.get(
    "/",
    response_model=List[CategoriaMaquinaResponse],
    summary="Listar categorías de máquinas",
)
def listar_categorias(
    db: Session = Depends(get_db),
    current_user: dict =Depends(require_roles("Administrador", "Entrenador")),
):
    return MaquinaRepository.get_all_categorias(db)


@router.post(
    "/",
    response_model=CategoriaMaquinaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría de máquina",
)
def crear_categoria(
    data: CategoriaMaquinaCreate,
    db: Session = Depends(get_db),
    current_user: dict =Depends(require_roles("Administrador")),
):
    return MaquinaRepository.create_categoria(db, data.nombre, data.descripcion)
