from fastapi import APIRouter 
 
router = APIRouter(prefix="/api/v1", tags=["Evaluaciones"]) 
 
@router.post("/clientes/{cliente_id}/evaluaciones") 
def registrar_evaluacion(cliente_id: int): 
    return {"mensaje": f"Evaluacion registrada para cliente {cliente_id}"} 
 
@router.get("/clientes/{cliente_id}/evaluaciones") 
def obtener_evaluaciones(cliente_id: int): 
    return {"mensaje": f"Evaluaciones del cliente {cliente_id}"} 
