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

router = APIRouter(prefix="/maquinas", tags=["Máquinas e Instalaciones"])

ESTADOS_VALIDOS = ["Activa", "En Mantenimiento", "Fuera de Servicio"]

@router.get(
    "/",
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
    "/",
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
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return MaquinaRepository.create(db, data)


@router.get(
    "/{maquina_id}",
    response_model=MaquinaResponse,
    summary="Obtener una máquina por su ID",
)
def obtener_maquina(
    maquina_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador")),
):
    maquina = MaquinaRepository.get_by_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return maquina



@router.put(
    "/{maquina_id}",
    response_model=MaquinaResponse,
    summary="Actualizar completamente una máquina",
)
def actualizar_maquina(
    maquina_id: int,
    data: MaquinaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    maquina = MaquinaRepository.update(db, maquina_id, data)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return maquina


@router.patch(
    "/{maquina_id}/estado",
    response_model=MaquinaResponse,
    summary="Cambiar el estado operativo de una máquina",
)
def cambiar_estado(
    maquina_id: int,
    data: MaquinaEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    if data.estado_operativo not in ESTADOS_VALIDOS:
        return bad_request_response(
            mensaje=f"Estado inválido. Valores permitidos: {ESTADOS_VALIDOS}",
            codigo_interno="ERR_ESTADO_INVALIDO"
        )
    maquina = MaquinaRepository.update_estado(db, maquina_id, data.estado_operativo)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return maquina

@router.delete(
    "/{maquina_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una máquina",
)
def eliminar_maquina(
    maquina_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    eliminado = MaquinaRepository.delete(db, maquina_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return None