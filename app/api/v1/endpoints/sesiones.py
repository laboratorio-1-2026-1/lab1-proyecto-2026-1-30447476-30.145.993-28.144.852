from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.core.dependencies import get_current_user, require_roles
from app.api.database.session import get_db
from app.api.models.sesion import Sesion
from app.api.schemas.sesion import SesionCreate, SesionResponse

router = APIRouter(prefix="/sesiones", tags=["Sesiones"])


@router.get("", response_model=list[SesionResponse])
def listar_sesiones(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    fecha: Optional[str] = None,
    disciplina: Optional[str] = None,
    current_user=Depends(get_current_user),
):
    query = db.query(Sesion)
    if fecha:
        query = query.filter(Sesion.fecha == fecha)
    if disciplina:
        query = query.filter(Sesion.disciplina.ilike(f"%{disciplina}%"))
    return query.offset(skip).limit(limit).all()


@router.post("", response_model=SesionResponse, status_code=201)
def crear_sesion(
    sesion_data: SesionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["Administrador", "Entrenador"])),
):
    nueva_sesion = Sesion(
        disciplina=sesion_data.disciplina,
        entrenador_id=sesion_data.entrenador_id,
        fecha=sesion_data.fecha,
        hora_inicio=sesion_data.hora_inicio,
        hora_fin=sesion_data.hora_fin,
        cupo_maximo=sesion_data.cupo_maximo,
        cupos_disponibles=sesion_data.cupo_maximo,
        estado="Programada",
    )
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    return nueva_sesion


@router.get("/{sesion_id}", response_model=SesionResponse)
def obtener_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return sesion