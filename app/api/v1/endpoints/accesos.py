from fastapi import APIRouter 
 
router = APIRouter(prefix="/api/v1", tags=["Accesos"]) 
 
@router.post("/accesos/entrada") 
def registrar_entrada(): 
    return {"mensaje": "Entrada registrada"} 
