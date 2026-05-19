from fastapi import APIRouter 
 
router = APIRouter(prefix="/api/v1", tags=["Pagos"]) 
 
@router.post("/pagos") 
def registrar_pago(): 
    return {"mensaje": "Pago registrado"} 
