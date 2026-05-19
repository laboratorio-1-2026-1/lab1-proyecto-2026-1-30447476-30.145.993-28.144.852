from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

# Schema para la reserva (esto es lo que permite el cuadro de texto)
class ReservaCreate(BaseModel):
    cliente_id: int
    sesion_id: int

router = APIRouter(prefix="/api/v1", tags=["Reservas"])

@router.get("/reservas")
def listar_reservas():
    return {"mensaje": "Lista de reservas"}

@router.post("/reservas", status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: ReservaCreate):
    # Aquí irá la lógica real después
    return {
        "mensaje": "Reserva creada",
        "cliente_id": reserva.cliente_id,
        "sesion_id": reserva.sesion_id,
        "fecha_reserva": datetime.now().isoformat()
    }