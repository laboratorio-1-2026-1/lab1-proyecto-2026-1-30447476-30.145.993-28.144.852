from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.services.cliente_service import ClienteService
from app.api.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador")),
):
    return ClienteService.crear(db, data, usuario_id=current_user.get("user_id"))

@router.get("/", response_model=dict)
def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Finanzas", "Entrenador")),
):
    return ClienteService.listar(db, skip, limit)

@router.get("/{cliente_id}", response_model=dict)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador", "Finanzas", "Entrenador")),
):
    return ClienteService.obtener(db, cliente_id)

@router.put("/{cliente_id}", response_model=dict)
def actualizar_cliente(
    cliente_id: int,
    data: ClienteUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return ClienteService.actualizar(db, cliente_id, data)

@router.delete("/{cliente_id}", response_model=dict)
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("Administrador")),
):
    return ClienteService.eliminar(db, cliente_id)