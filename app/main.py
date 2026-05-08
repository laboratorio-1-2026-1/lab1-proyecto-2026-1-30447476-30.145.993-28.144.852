from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import init_db
from app.api.v1.routers import api_router

# Inicializar BD
init_db()

# Crear aplicación
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gestión integral de gimnasios"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "mensaje": "Bienvenido a SmartGym API",
        "version": settings.VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

# Health check
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )