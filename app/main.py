from fastapi import FastAPI
from app.api.database.session import engine, Base

from app.api.v1.endpoints.maquinas import router as maquinas_router
from app.api.v1.endpoints.categoriasMaquinas import router as categoriasMaquinas_router
from app.api.v1.endpoints.ticketsMantenimiento import router as ticketsMantenimiento_router
from app.api.v1.endpoints.productos import router as productos_router
from app.api.v1.endpoints.ventas import router as ventas_router
from app.api.v1.endpoints.categoriaProducto import router as categoriaProducto_router

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartGym API")

app.include_router(maquinas_router, prefix="/api/v1")
app.include_router(categoriasMaquinas_router, prefix="/api/v1")
app.include_router(ticketsMantenimiento_router, prefix="/api/v1")
app.include_router(productos_router, prefix="/api/v1")
app.include_router(ventas_router, prefix="/api/v1")
app.include_router(categoriaProducto_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"} 
