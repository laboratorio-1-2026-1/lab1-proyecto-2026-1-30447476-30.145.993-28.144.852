from app.api.repositories.venta_repository import VentaRepository
from app.api.repositories.producto_repository import ProductoRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timezone

class VentaService:
    def __init__(self, db: Session):
        self.db = db
        self.venta_repo = VentaRepository()
        self.producto_repo = ProductoRepository()

    def registrar_venta(
        self,
        usuario_id: int,
        cliente_id: int,
        items: List[Dict[str, Any]],
        metodo_pago: str
    ) -> Dict[str, Any]:
        # Validar que haya al menos un ítem
        if not items or len(items) == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_VENTA_SIN_ITEMS",
                    "mensaje": "La venta debe incluir al menos un producto.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )

        # Validar método de pago
        metodos_validos = ["efectivo", "tarjeta", "transferencia", "credito"]
        if metodo_pago.lower() not in metodos_validos:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_METODO_PAGO_INVALIDO",
                    "mensaje": f"Método de pago '{metodo_pago}' no válido. Métodos permitidos: {', '.join(metodos_validos)}",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )

        # Validar existencia y stock de productos
        items_para_repo = []
        for item in items:
            producto = self.producto_repo.get_by_id(self.db, item["producto_id"])
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "error": "Not Found",
                        "codigoInterno": "ERR_PRODUCTO_NO_ENCONTRADO",
                        "mensaje": f"Producto con ID {item['producto_id']} no encontrado.",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
            if not producto.activo:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "error": "Conflict",
                        "codigoInterno": "ERR_PRODUCTO_INACTIVO",
                        "mensaje": f"El producto '{producto.nombre}' no está disponible para la venta.",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
            if producto.stock < item["cantidad"]:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "error": "Conflict",
                        "codigoInterno": "ERR_STOCK_INSUFICIENTE",
                        "mensaje": f"Stock insuficiente para '{producto.nombre}'. "
                                   f"Disponible: {producto.stock}, solicitado: {item['cantidad']}",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
            items_para_repo.append({
                "producto_id": item["producto_id"],
                "cantidad": item["cantidad"]
            })

        # Crear la venta (el repositorio genera número de venta, fecha, y descuenta stock)
        try:
            venta = self.venta_repo.create(
                db=self.db,
                usuario_id=usuario_id,
                items=items_para_repo,
                cliente_id=cliente_id,
                metodoPago=metodo_pago
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_VENTA_FALLIDA",
                    "mensaje": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )

        # Preparar detalles de la venta para la respuesta
        detalles = []
        for detalle in venta.ventaDetalles:
            detalles.append({
                "producto_id": detalle.producto_id,
                "cantidad": detalle.cantidad,
                "precio_unitario": float(detalle.precioUnitario),
                "subtotal": float(detalle.subtotal)
            })

        return {
            "status": "success",
            "mensaje": "Venta registrada exitosamente.",
            "data": {
                "id": venta.idVenta,
                "numeroVenta": venta.numeroVenta,
                "fechaVenta": venta.fechaVenta.isoformat(),
                "montoTotal": float(venta.montoTotal),
                "metodoPago": venta.metodoPago,
                "estado": venta.estado.value if hasattr(venta.estado, 'value') else venta.estado,
                "cliente_id": venta.cliente_id,
                "usuario_id": venta.usuario_id,
                "items": detalles
            }
        }

    def listar_ventas(self, skip: int = 0, limit: int = 100) -> List[VentaResponse]:
        from app.api.schemas.venta import VentaResponse
        ventas = self.venta_repo.get_all(self.db, skip=skip, limit=limit)
        return [VentaResponse.model_validate(v) for v in ventas]

    def obtener_venta(self, venta_id: int) -> VentaResponse:
        from app.api.schemas.venta import VentaResponse
        venta = self.venta_repo.get_by_id(self.db, venta_id)
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        return VentaResponse.model_validate(venta)