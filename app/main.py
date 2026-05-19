from fastapi import FastAPI 
from app.api.v1.endpoints import sesiones 
from app.api.v1.endpoints import reservas 
from app.api.v1.endpoints import accesos 
from app.api.v1.endpoints import planes 
from app.api.v1.endpoints import pagos 
from app.api.v1.endpoints import evaluaciones 
 
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
