from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, List
from datetime import datetime, timezone
from app.api.repositories.producto_repository import ProductoRepository
from app.api.repositories.categoriaProducto_repository import CategoriaProductoRepository
from app.api.schemas.producto import ProductoCreate, ProductoUpdate
from app.api.models.producto import ProductoTienda


class ProductoService:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: ProductoCreate):
        # Validar que la categoría exista (regla de negocio)
        categoria = CategoriaProductoRepository.get_by_id(self.db, data.categoriaProducto_id)
        if not categoria:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_CATEGORIA_NO_VALIDA",
                    "mensaje": f"Categoría de producto con ID {data.categoriaProducto_id} no válida o no existe.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        
        # Validar código de barras único (regla de negocio)
        if data.codigoBarra:
            existente = ProductoRepository.get_by_codigoBarra(self.db, data.codigoBarra)
            if existente:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": "Conflict",
                        "codigoInterno": "ERR_CODIGOBARRA_DUPLICADO",
                        "mensaje": f"Ya existe un producto con el código de barras '{data.codigoBarra}'.",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
        
        # Crear el producto
        producto_creado = ProductoRepository.create(self.db, data)
        
        return {
            "status": "success",
            "mensaje": "Producto creado exitosamente.",
            "data": {
                "id": producto_creado.idProductosTienda,
                "nombre": producto_creado.nombre,
                "descripcion": producto_creado.descripcion if hasattr(producto_creado, 'descripcion') else None,  # ← AGREGADO
                "codigoBarra": producto_creado.codigoBarra,
                "categoriaProducto_id": producto_creado.categoriaProducto_id,
                "activo": producto_creado.activo,
                "precio": float(producto_creado.precio),
                "stock": producto_creado.stock,
                "created_at": producto_creado.created_at.isoformat() if hasattr(producto_creado, 'created_at') and producto_creado.created_at else None  # ← AGREGADO
            }
        }

    def listar(self, activo: Optional[bool] = None, skip: int = 0, limit: int = 100):
        productos = ProductoRepository.get_all(
            self.db,
            solo_activos=activo if activo is not None else True,
            skip=skip,
            limit=limit
        )
        
        return {
            "status": "success",
            "mensaje": f"Se encontraron {len(productos)} productos.",
            "data": [
                {
                    "id": p.idProductosTienda,
                    "nombre": p.nombre,
                    "descripcion": p.descripcion if hasattr(p, 'descripcion') else None,  # ← AGREGADO
                    "codigoBarra": p.codigoBarra,
                    "categoriaProducto_id": p.categoriaProducto_id,
                    "activo": p.activo,
                    "precio": float(p.precio) if p.precio else None,
                    "stock": p.stock if p.stock else None,
                    "created_at": p.created_at.isoformat() if hasattr(p, 'created_at') and p.created_at else None  # ← AGREGADO
                }
                for p in productos
            ]
        }

    def obtener(self, producto_id: int):
        producto = ProductoRepository.get_by_id(self.db, producto_id)
        if not producto:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Not Found",
                    "codigoInterno": "ERR_PRODUCTO_NO_ENCONTRADO",
                    "mensaje": f"Producto con ID {producto_id} no encontrado.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        
        return {
            "status": "success",
            "mensaje": "Producto encontrado.",
            "data": {
                "id": producto.idProductosTienda,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion if hasattr(producto, 'descripcion') else None,
                "codigoBarra": producto.codigoBarra,
                "categoriaProducto_id": producto.categoriaProducto_id,
                "activo": producto.activo,
                "precio": float(producto.precio) if producto.precio else None,
                "stock": producto.stock if producto.stock else None,
                "created_at": producto.created_at.isoformat() if hasattr(producto, 'created_at') and producto.created_at else None,
                "updated_at": producto.updated_at.isoformat() if hasattr(producto, 'updated_at') and producto.updated_at else None
            }
        }

    def actualizar(self, producto_id: int, data: ProductoUpdate):
        # Verificar existencia
        producto_existente = ProductoRepository.get_by_id(self.db, producto_id)
        if not producto_existente:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Not Found",
                    "codigoInterno": "ERR_PRODUCTO_NO_ENCONTRADO",
                    "mensaje": f"Producto con ID {producto_id} no encontrado.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        
        # Validar código de barras único si se está actualizando
        if data.codigoBarra:
            existente = ProductoRepository.get_by_codigoBarra(self.db, data.codigoBarra)
            if existente and existente.idProductosTienda != producto_id:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": "Conflict",
                        "codigoInterno": "ERR_CODIGOBARRA_DUPLICADO",
                        "mensaje": f"El código de barras '{data.codigoBarra}' ya está en uso por otro producto.",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
        
        # Validar categoría si se actualiza
        if data.categoriaProducto_id:
            categoria = CategoriaProductoRepository.get_by_id(self.db, data.categoriaProducto_id)
            if not categoria:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": "Conflict",
                        "codigoInterno": "ERR_CATEGORIA_NO_VALIDA",
                        "mensaje": f"Categoría de producto con ID {data.categoriaProducto_id} no válida o no existe.",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
        
        # Actualizar el producto
        producto_actualizado = ProductoRepository.update(self.db, producto_id, data)
        
        return {
            "status": "success",
            "mensaje": "Producto actualizado exitosamente.",
            "data": {
                "id": producto_actualizado.idProductosTienda,
                "nombre": producto_actualizado.nombre,
                "descripcion": producto_actualizado.descripcion if hasattr(producto_actualizado, 'descripcion') else None,  # ← AGREGADO
                "codigoBarra": producto_actualizado.codigoBarra,
                "categoriaProducto_id": producto_actualizado.categoriaProducto_id,
                "activo": producto_actualizado.activo,
                "precio": float(producto_actualizado.precio) if producto_actualizado.precio else None,
                "stock": producto_actualizado.stock if producto_actualizado.stock else None,
                "created_at": producto_actualizado.created_at.isoformat() if hasattr(producto_actualizado, 'created_at') and producto_actualizado.created_at else None,  # ← AGREGADO
                "updated_at": producto_actualizado.updated_at.isoformat() if hasattr(producto_actualizado, 'updated_at') and producto_actualizado.updated_at else None
            }
        }

    def actualizar_stock(self, producto_id: int, nuevo_stock: int):
        if nuevo_stock < 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Bad Request",
                    "codigoInterno": "ERR_STOCK_NEGATIVO",
                    "mensaje": "El stock no puede ser negativo.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        
        producto = ProductoRepository.get_by_id(self.db, producto_id)
        if not producto:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Not Found",
                    "codigoInterno": "ERR_PRODUCTO_NO_ENCONTRADO",
                    "mensaje": f"Producto con ID {producto_id} no encontrado.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        
        producto_actualizado = ProductoRepository.update_stock(self.db, producto_id, nuevo_stock)
        
        return {
            "status": "success",
            "mensaje": "Stock actualizado exitosamente.",
            "data": {
                "id": producto_actualizado.idProductosTienda,
                "nombre": producto_actualizado.nombre,
                "stock": producto_actualizado.stock,
                "updated_at": producto_actualizado.updated_at.isoformat() if hasattr(producto_actualizado, 'updated_at') and producto_actualizado.updated_at else None
            }
        }

    def eliminar(self, producto_id: int):
        producto = ProductoRepository.get_by_id(self.db, producto_id)
        if not producto:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Not Found",
                    "codigoInterno": "ERR_PRODUCTO_NO_ENCONTRADO",
                    "mensaje": f"Producto con ID {producto_id} no encontrado.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        
        if not ProductoRepository.desactivar(self.db, producto_id):
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Not Found",
                    "codigoInterno": "ERR_PRODUCTO_NO_ENCONTRADO",
                    "mensaje": f"Producto con ID {producto_id} no encontrado.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        
        return {
            "status": "success",
            "mensaje": "Producto eliminado exitosamente.",
            "data": None
        }