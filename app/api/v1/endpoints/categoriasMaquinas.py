from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.schemas.categoriasMaquinas import (
    CategoriaMaquinaCreate,
    CategoriaMaquinaResponse)
from app.api.repositories.maquina_repository import MaquinaRepository

router = APIRouter(prefix="/api/v1", tags=["Máquinas e Instalaciones"])


@router.get(
    "/categorias-maquinas",
    response_model=List[CategoriaMaquinaResponse],
    summary="Listar categorías de máquinas",
)
def listar_categorias(
    db: Session = Depends(get_db),
     current_user: dict =Depends(require_roles("Administrador", "Entrenador")),
):
    return MaquinaRepository.get_all_categorias(db)


@router.post(
    "/categorias-maquinas",
    response_model=CategoriaMaquinaResponse,
    status_code=201,
    summary="Crear categoría de máquina",
)
def crear_categoria(
    data: CategoriaMaquinaCreate,
    db: Session = Depends(get_db),
     current_user: dict =Depends(require_roles("Administrador")),
):
    return MaquinaRepository.create_categoria(db, data.nombre, data.descripcion)