from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import PlanSuscripcion, MembresiaCliente, Pago
from app.repositories.base_repository import BaseRepository


class PlanRepository(BaseRepository[PlanSuscripcion]):

    def __init__(self):
        super().__init__(PlanSuscripcion)

    def get_activos(self, db: Session) -> List[PlanSuscripcion]:
        return (
            db.query(PlanSuscripcion)
            .filter(PlanSuscripcion.activo == True)
            .order_by(PlanSuscripcion.precio)
            .all()
        )

    def get_by_nombre(self, db: Session, nombre: str) -> Optional[PlanSuscripcion]:
        return (
            db.query(PlanSuscripcion)
            .filter(PlanSuscripcion.nombre == nombre)
            .first()
        )


class MembresiaRepository(BaseRepository[MembresiaCliente]):

    def __init__(self):
        super().__init__(MembresiaCliente)

    def get_ultima_por_cliente(
        self, db: Session, cliente_id: int
    ) -> Optional[MembresiaCliente]:
        """Membresía más reciente (por fecha de fin) del cliente."""
        return (
            db.query(MembresiaCliente)
            .filter(MembresiaCliente.cliente_id == cliente_id)
            .order_by(MembresiaCliente.fechaFin.desc())
            .first()
        )

    def get_todas_por_cliente(
        self, db: Session, cliente_id: int
    ) -> List[MembresiaCliente]:
        return (
            db.query(MembresiaCliente)
            .filter(MembresiaCliente.cliente_id == cliente_id)
            .order_by(MembresiaCliente.fechaInicio.desc())
            .all()
        )

    def crear(
        self, db: Session, cliente_id: int, plan_id: int, duracion_dias: int
    ) -> MembresiaCliente:
        hoy = date.today()
        membresia = MembresiaCliente(
            cliente_id=cliente_id,
            plan_id=plan_id,
            fechaInicio=hoy,
            fechaFin=hoy + timedelta(days=duracion_dias),
        )
        db.add(membresia)
        db.flush()  # obtener ID sin hacer commit todavía
        return membresia

    def estado(self, membresia: MembresiaCliente) -> str:
        """Calcula el estado actual: Activa | Por Vencer | Vencida."""
        hoy = date.today()
        if membresia.fechaFin < hoy:
            return "Vencida"
        if (membresia.fechaFin - hoy).days <= 7:
            return "Por Vencer"
        return "Activa"


class PagoRepository(BaseRepository[Pago]):

    def __init__(self):
        super().__init__(Pago)

    def get_por_cliente(self, db: Session, cliente_id: int) -> List[Pago]:
        return (
            db.query(Pago)
            .filter(Pago.cliente_id == cliente_id)
            .order_by(Pago.fechaPago.desc())
            .all()
        )

    def get_por_periodo(
        self, db: Session, fecha_inicio: date, fecha_fin: date
    ) -> List[Pago]:
        return (
            db.query(Pago)
            .filter(
                Pago.fechaPago >= str(fecha_inicio),
                Pago.fechaPago <= str(fecha_fin),
            )
            .order_by(Pago.fechaPago.desc())
            .all()
        )

    def crear_inmutable(
        self,
        db: Session,
        cliente_id: int,
        membresia_id: int,
        plan: PlanSuscripcion,
        monto_pagado: Decimal,
        metodo_pago: Optional[str],
        referencia: Optional[str],
        descripcion: Optional[str],
    ) -> Pago:
        """
        Regla de negocio: el pago guarda un SNAPSHOT inmutable del
        nombre y precio del plan en el momento de la transacción.
        Nunca se permite UPDATE ni DELETE sobre esta tabla.
        """
        pago = Pago(
            cliente_id=cliente_id,
            membresia_id=membresia_id,
            plan_id=plan.idPlanesSuscripcion,
            nombre_plan_snapshot=plan.nombre,   # inmutable
            precio_plan_snapshot=plan.precio,   # inmutable
            montoPagado=monto_pagado,
            metodoPago=metodo_pago,
            referencia=referencia,
            descripcion=descripcion,
        )
        db.add(pago)
        db.commit()
        db.refresh(pago)
        return pago


plan_repository = PlanRepository()
membresia_repository = MembresiaRepository()
pago_repository = PagoRepository()