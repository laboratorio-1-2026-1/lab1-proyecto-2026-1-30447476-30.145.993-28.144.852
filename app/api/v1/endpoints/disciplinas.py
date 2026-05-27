from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.services.disciplina_service import DisciplinaService
from app.api.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_disciplina(
    data: DisciplinaCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return DisciplinaService.crear(db, data)

@router.get("/", response_model=dict)
def listar_disciplinas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    return DisciplinaService.listar(db, skip, limit)

@router.get("/{disciplina_id}", response_model=dict)
def obtener_disciplina(
    disciplina_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    return DisciplinaService.obtener(db, disciplina_id)

@router.put("/{disciplina_id}", response_model=dict)
def actualizar_disciplina(
    disciplina_id: int,
    data: DisciplinaUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return DisciplinaService.actualizar(db, disciplina_id, data)

@router.delete("/{disciplina_id}", response_model=dict)
def eliminar_disciplina(
    disciplina_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return DisciplinaService.eliminar(db, disciplina_id)