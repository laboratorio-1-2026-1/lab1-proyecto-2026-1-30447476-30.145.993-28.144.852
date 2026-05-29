from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api.database.session import get_db
from app.api.core.security import require_roles, get_current_user
from app.api.services.evaluacion_service import EvaluacionService
from app.api.schemas.evaluacion import EvaluacionCreate, EvaluacionUpdate

router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones Biometricas"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_evaluacion(
    data: EvaluacionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador")),
):
    return EvaluacionService.crear(db, data, current_user["rol"], current_user["user_id"])

@router.get("/", response_model=dict)
def listar_evaluaciones(
    skip: int = 0,
    limit: int = 100,
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente (solo admin/entrenador)"),
    entrenador_id: Optional[int] = Query(None, description="Filtrar por entrenador (solo admin)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    
    return EvaluacionService.listar(db, skip, limit, current_user["rol"], current_user["user_id"], cliente_id, entrenador_id)

@router.get("/{evaluacion_id}", response_model=dict)
def obtener_evaluacion(
    evaluacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    return EvaluacionService.obtener(db, evaluacion_id, current_user["rol"], current_user["user_id"])

@router.put("/{evaluacion_id}", response_model=dict)
def actualizar_evaluacion(
    evaluacion_id: int,
    data: EvaluacionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador")),
):
    return EvaluacionService.actualizar(db, evaluacion_id, data, current_user["rol"], current_user["user_id"])

@router.delete("/{evaluacion_id}", response_model=dict)
def eliminar_evaluacion(
    evaluacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador")),
):
    return EvaluacionService.eliminar(db, evaluacion_id, current_user["rol"], current_user["user_id"])