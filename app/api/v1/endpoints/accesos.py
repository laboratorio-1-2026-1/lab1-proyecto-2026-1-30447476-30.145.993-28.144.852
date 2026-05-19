from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.database.session import get_db
from app.api.schemas.acceso import AccesoCreate, AccesoResponse
from app.api.services.acceso_service import acceso_service

router = APIRouter(prefix="/accesos", tags=["Accesos"])


@router.get("", response_model=List[AccesoResponse])
def listar_accesos(db: Session = Depends(get_db)):
    return acceso_service.listar(db)


@router.post("/entrada", response_model=AccesoResponse)
def registrar_entrada(datos: AccesoCreate, db: Session = Depends(get_db)):
    return acceso_service.registrar_entrada(db, datos.documento_identidad)
