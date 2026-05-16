from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.usuarios import router as usuarios_router
from app.api.v1.endpoints.maquinas import router as maquinas_router
from app.api.v1.endpoints.categoriasMaquinas import router as categoriasMaquinas_router
from app.api.v1.endpoints.ticketsMantenimiento import router as ticketsMantenimiento_router
from app.api.v1.endpoints.productos import router as productos_router
from app.api.v1.endpoints.ventas import router as ventas_router
from app.api.v1.endpoints.categoriaProducto import router as categoriaProducto_router

# Router principal
router = APIRouter()

router.include_router(auth_router, prefix="/api/v1", tags=["Autenticación"])
router.include_router(usuarios_router, prefix="/api/v1", tags=["Usuarios"])
router.include_router(categoriasMaquinas_router, prefix="/api/v1", tags=["Categorías de Máquinas"])
router.include_router(maquinas_router, prefix="/api/v1", tags=["Máquinas"])
router.include_router(ticketsMantenimiento_router, prefix="/api/v1", tags=["Mantenimiento"])
router.include_router(productos_router, prefix="/api/v1", tags=["Productos"])
router.include_router(ventas_router, prefix="/api/v1", tags=["Ventas"])
router.include_router(categoriaProducto_router, prefix="/api/v1", tags=["Categorías de Productos"])