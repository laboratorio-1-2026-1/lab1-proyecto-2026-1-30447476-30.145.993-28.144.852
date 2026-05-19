from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from app.api.core.database import get_db 
from app.api.schemas.plan import PlanCreate, PlanResponse 
from app.api.models.plan import Plan 
 
router = APIRouter(prefix="/planes", tags=["Planes"]) 
 
@router.get("", response_model=list[PlanResponse]) 
def listar_planes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100): 
    return db.query(Plan).offset(skip).limit(limit).all() 
 
@router.post("", response_model=PlanResponse, status_code=201) 
def crear_plan(plan_data: PlanCreate, db: Session = Depends(get_db)): 
    nuevo_plan = Plan( 
        nombre=plan_data.nombre, 
        precio=plan_data.precio, 
        duracion_dias=plan_data.duracion_dias 
    ) 
    db.add(nuevo_plan) 
    db.commit() 
    db.refresh(nuevo_plan) 
