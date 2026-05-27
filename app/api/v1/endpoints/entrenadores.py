from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.services.entrenador_service import EntrenadorService
from app.api.schemas.entrenador import EntrenadorCreate, EntrenadorUpdate, EntrenadorResponse

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_entrenador(
    data: EntrenadorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    usuario_id = current_user.get("user_id")
    return EntrenadorService.crear(db, data, usuario_id)

@router.get("/", response_model=dict)
def listar_entrenadores(
    skip: int = 0,
    limit: int = 100,
    solo_activos: bool = True,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    return EntrenadorService.listar(db, skip, limit, solo_activos)

@router.get("/{entrenador_id}", response_model=dict)
def obtener_entrenador(
    entrenador_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    return EntrenadorService.obtener(db, entrenador_id)

@router.put("/{entrenador_id}", response_model=dict)
def actualizar_entrenador(
    entrenador_id: int,
    data: EntrenadorUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return EntrenadorService.actualizar(db, entrenador_id, data)

@router.delete("/{entrenador_id}", response_model=dict)
def eliminar_entrenador(
    entrenador_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return EntrenadorService.eliminar(db, entrenador_id)