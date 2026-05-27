from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.models.venta import Venta
from app.api.models.ventaDetalle import VentaDetalle
from app.api.models.producto import ProductoTienda


class VentaRepository:

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Venta]:
        return db.query(Venta).order_by(Venta.fechaVenta.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, venta_id: int) -> Optional[Venta]:
        return db.query(Venta).filter(Venta.idVenta == venta_id).first()

    @staticmethod
    def get_by_cliente(
        db: Session,
        cliente_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Venta]:
        return db.query(Venta).filter(Venta.cliente_id == cliente_id).order_by(Venta.fechaVenta.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_usuario(
        db: Session,
        usuario_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Venta]:
        """Opcional: listar ventas realizadas por un usuario (vendedor)"""
        return db.query(Venta).filter(Venta.usuario_id == usuario_id).order_by(Venta.fechaVenta.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create(
        db: Session,
        usuario_id: int,
        items: List[dict],          # [{"producto_id": int, "cantidad": int}]
        cliente_id: Optional[int] = None,
        metodoPago: Optional[str] = None,
    ) -> Venta:
        """
        Crea la venta y sus detalles en una sola transacción.
        Asume que el stock ya fue validado antes de llamar este método.
        """
        total = Decimal("0.00")
        detalles_data = []

        for item in items:
            producto = db.query(ProductoTienda).filter(
                ProductoTienda.idProductosTienda == item["producto_id"]
            ).first()
            if not producto:
                raise ValueError(f"Producto con id {item['producto_id']} no existe")

            precioUnitario = producto.precio
            subtotal = precioUnitario * item["cantidad"]
            total += subtotal

            # Descontar stock dentro de la misma transacción
            producto.stock -= item["cantidad"]

            detalles_data.append({
                "producto_id": item["producto_id"],
                "cantidad": item["cantidad"],
                "precioUnitario": precioUnitario,
                "subtotal": subtotal,
            })


        numero_venta = f"VENTA-{int(datetime.now().timestamp())}"

        venta = Venta(
            numeroVenta=numero_venta,
            fechaVenta=datetime.now(),
            cliente_id=cliente_id,
            usuario_id=usuario_id,    
            montoTotal=total,              
            metodoPago=metodoPago,
        )
        db.add(venta)
        db.flush()  # obtener idVenta

        for d in detalles_data:
            detalle = VentaDetalle(
                venta_id=venta.idVenta,
                producto_id=d["producto_id"],
                cantidad=d["cantidad"],
                precioUnitario=d["precioUnitario"],
                subtotal=d["subtotal"],
            )
            db.add(detalle)

        db.commit()
        db.refresh(venta)
        return venta

    @staticmethod
    def get_detalles(db: Session, venta_id: int) -> List[VentaDetalle]:
        return db.query(VentaDetalle).filter(VentaDetalle.venta_id == venta_id).all()