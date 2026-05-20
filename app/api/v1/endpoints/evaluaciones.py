from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.schemas.evaluacion import EvaluacionCreate, EvaluacionResponse
from app.api.services.evaluacion_service import EvaluacionService

router = APIRouter(tags=["Evaluaciones"])


@router.post(
    "/clientes/{cliente_id}/evaluaciones",
    response_model=EvaluacionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar evaluación biométrica",
)
def registrar_evaluacion(
    cliente_id: int,
    data: EvaluacionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador")),
):
    return EvaluacionService().registrar_evaluacion(
        db=db,
        cliente_id=cliente_id,
        entrenador_id=current_user["user_id"],
        peso=data.peso,
        estatura=data.estatura,
        grasa_corporal=data.grasa_corporal,
        observaciones=data.observaciones,
    )


@router.get(
    "/clientes/{cliente_id}/evaluaciones",
    response_model=List[EvaluacionResponse],
    summary="Historial de evaluaciones de un cliente",
)
def obtener_evaluaciones(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    return EvaluacionService().obtener_historial_cliente(db, cliente_id)
