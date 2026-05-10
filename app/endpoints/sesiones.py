from fastapi import APIRouter 
 
router = APIRouter(prefix="/api/v1", tags=["Sesiones"]) 
 
@router.get("/sesiones") 
def listar_sesiones(): 
    return {"mensaje": "Lista de sesiones - Prueba funcionando"} 
