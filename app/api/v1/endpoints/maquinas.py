from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.core.errors import conflict_response, bad_request_response
from app.api.schemas.maquina import (
    MaquinaCreate,
    MaquinaUpdate,
    MaquinaEstadoUpdate,
    MaquinaResponse,
)
from app.api.repositories.maquina_repository import MaquinaRepository

router = APIRouter(prefix="/api/v1", tags=["Máquinas e Instalaciones"])

ESTADOS_VALIDOS = ["Activa", "En Mantenimiento", "Fuera de Servicio"]

@router.get(
    "/maquinas",
    response_model=List[MaquinaResponse],
    summary="Listar máquinas (filtros opcionales: categoria_id, estado)",
)
def listar_maquinas(
    categoria_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador")),
):
    if estado and estado not in ESTADOS_VALIDOS:
        return bad_request_response(
            mensaje=f"Estado inválido. Valores permitidos: {ESTADOS_VALIDOS}",
            codigo_interno="ERR_ESTADO_INVALIDO"
        )
    return MaquinaRepository.get_all(db, categoria_id=categoria_id, estado=estado)

@router.post(
    "/maquinas",
    response_model=MaquinaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nueva máquina",
)
def crear_maquina(
    data: MaquinaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    if not MaquinaRepository.get_categoria_by_id(db, data.categoria_id):
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    return MaquinaRepository.create(db, data)