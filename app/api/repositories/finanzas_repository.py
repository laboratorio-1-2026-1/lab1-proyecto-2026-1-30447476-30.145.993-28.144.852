from datetime import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.models.pago import Pago
from app.api.models.venta import Venta


class FinanzasRepository:

    @staticmethod
    def ingresos_por_periodo(
        db: Session,
        fecha_inicio: datetime,
        fecha_fin: datetime,
    ) -> dict:
        """
        Suma total de ingresos (pagos de membresía + ventas de tienda)
        dentro de un rango de fechas dado.
        """
        total_membresias = (
            db.query(func.sum(Pago.monto))
            .filter(
                Pago.fecha_pago >= fecha_inicio,
                Pago.fecha_pago <= fecha_fin,
            )
            .scalar() or 0.0
        )

        total_tienda = (
            db.query(func.sum(Venta.total))
            .filter(
                Venta.fecha_venta >= fecha_inicio,
                Venta.fecha_venta <= fecha_fin,
            )
            .scalar() or 0.0
        )

        return {
            "fecha_inicio":        fecha_inicio.isoformat(),
            "fecha_fin":           fecha_fin.isoformat(),
            "ingresos_membresias": round(float(total_membresias), 2),
            "ingresos_tienda":     round(float(total_tienda), 2),
            "total_general":       round(float(total_membresias) + float(total_tienda), 2),
        }

    @staticmethod
    def pagos_del_periodo(
        db: Session,
        fecha_inicio: datetime,
        fecha_fin: datetime,
    ) -> List[Pago]:
        """Lista detallada de pagos de membresía en el período."""
        return (
            db.query(Pago)
            .filter(
                Pago.fecha_pago >= fecha_inicio,
                Pago.fecha_pago <= fecha_fin,
            )
            .order_by(Pago.fecha_pago.desc())
            .all()
        )

    @staticmethod
    def clientes_con_membresia_activa(db: Session) -> int:
        ahora = datetime.now()
        return (
            db.query(func.count(func.distinct(Pago.cliente_id)))
            .filter(Pago.fecha_vencimiento >= ahora)
            .scalar() or 0
        )

    @staticmethod
    def clientes_con_membresia_vencida(db: Session) -> int:
        ahora = datetime.now()
        subq_activos = (
            db.query(Pago.cliente_id)
            .filter(Pago.fecha_vencimiento >= ahora)
            .subquery()
        )
        return (
            db.query(func.count(func.distinct(Pago.cliente_id)))
            .filter(Pago.cliente_id.notin_(subq_activos))
            .scalar() or 0
        )


finanzas_repository = FinanzasRepository() 
