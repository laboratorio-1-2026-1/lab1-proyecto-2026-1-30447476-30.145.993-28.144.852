from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.database.session import get_db
from app.api.core.security import require_roles
from app.api.models.sesion import Sesion
from app.api.models.disciplina import Disciplina
from app.api.schemas.sesion import SesionCreate, SesionResponse

router = APIRouter(prefix="/sesiones", tags=["Sesiones"])

@router.get("/", response_model=List[SesionResponse])
def listar_sesiones(
    skip: int = 0,
    limit: int = 100,
    fecha: Optional[str] = None,
    disciplina: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    query = db.query(Sesion)
    if fecha:
        query = query.filter(Sesion.fecha_hora_inicio >= fecha)
    if disciplina:
        # Buscar por nombre de disciplina 
        query = query.join(Disciplina).filter(Disciplina.nombre.ilike(f"%{disciplina}%"))
    sesiones = query.offset(skip).limit(limit).all()
    
    
    result = []
    for s in sesiones:
        result.append(SesionResponse(
            id=s.id,
            disciplina=s.disciplina.nombre,
            entrenador_id=s.entrenador_id,
            fecha=s.fecha_hora_inicio,
            hora_inicio=s.fecha_hora_inicio.time(),
            hora_fin=s.fecha_hora_fin.time(),
            cupo_maximo=s.cupo_maximo,
            cupos_disponibles=s.cupos_disponibles,
        ))
    return result

@router.post("/", response_model=SesionResponse, status_code=status.HTTP_201_CREATED)
def crear_sesion(
    data: SesionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador")),
):
    # Buscar la disciplina por nombre
    disciplina = db.query(Disciplina).filter(Disciplina.nombre == data.disciplina).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail=f"Disciplina '{data.disciplina}' no encontrada")
    

    fecha_hora_inicio = datetime.combine(data.fecha.date(), data.hora_inicio)
    fecha_hora_fin = datetime.combine(data.fecha.date(), data.hora_fin)
    
    if fecha_hora_fin <= fecha_hora_inicio:
        raise HTTPException(status_code=400, detail="La hora de fin debe ser mayor a la hora de inicio")
    
    nueva_sesion = Sesion(
        disciplina_id=disciplina.idDisciplina,
        entrenador_id=data.entrenador_id,
        fecha_hora_inicio=fecha_hora_inicio,
        fecha_hora_fin=fecha_hora_fin,
        cupo_maximo=data.cupo_maximo,
        cupos_disponibles=data.cupo_maximo,
        estado="Programada",
    )
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    
    
    return SesionResponse(
        id=nueva_sesion.id,
        disciplina=disciplina.nombre,
        entrenador_id=nueva_sesion.entrenador_id,
        fecha=nueva_sesion.fecha_hora_inicio,
        hora_inicio=nueva_sesion.fecha_hora_inicio.time(),
        hora_fin=nueva_sesion.fecha_hora_fin.time(),
        cupo_maximo=nueva_sesion.cupo_maximo,
        cupos_disponibles=nueva_sesion.cupos_disponibles,
    )

@router.get("/{sesion_id}", response_model=SesionResponse)
def obtener_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("Administrador", "Entrenador", "Cliente")),
):
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return SesionResponse(
        id=sesion.id,
        disciplina=sesion.disciplina.nombre,
        entrenador_id=sesion.entrenador_id,
        fecha=sesion.fecha_hora_inicio,
        hora_inicio=sesion.fecha_hora_inicio.time(),
        hora_fin=sesion.fecha_hora_fin.time(),
        cupo_maximo=sesion.cupo_maximo,
        cupos_disponibles=sesion.cupos_disponibles,
    )