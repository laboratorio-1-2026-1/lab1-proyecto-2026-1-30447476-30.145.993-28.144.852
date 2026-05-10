from fastapi import APIRouter 
 
router = APIRouter(prefix="/api/v1", tags=["Planes"]) 
 
@router.get("/planes") 
def listar_planes(): 
    return {"mensaje": "Lista de planes"} 
 
@router.post("/planes") 
def crear_plan(): 
    return {"mensaje": "Plan creado"} 
