from fastapi import FastAPI 
from app.endpoints import sesiones, reservas, accesos, planes, pagos, evaluaciones 
 
app = FastAPI(docs_url="/api-docs") 
 
app.include_router(sesiones.router) 
app.include_router(reservas.router) 
app.include_router(accesos.router) 
app.include_router(planes.router) 
app.include_router(pagos.router) 
app.include_router(evaluaciones.router) 
 
@app.get("/") 
def root(): 
    return {"message": "SmartGym API funcionando"} 
