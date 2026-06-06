from datetime import datetime, timedelta

from app.api.repositories.pago_repository import PagoRepository
from app.api.repositories.plan_repository import PlanRepository
from app.api.schemas.pago import PagoCreate

DIAS_POR_VENCER = 7


class PagoService:
    def __init__(self):
        self.pago_repo = PagoRepository()
        self.plan_repo = PlanRepository()

    def registrar_pago(self, db, cliente_id: int, plan_id: int, monto: float):
        plan = self.plan_repo.get_by_id(db, plan_id)
        if not plan:
            return {"success": False, "mensaje": "Plan no existe"}

        fecha_pago = datetime.now()
        fecha_vencimiento = fecha_pago + timedelta(days=plan.duracion_dias)

        pago_data = PagoCreate(
            cliente_id=cliente_id,
            plan_id=plan_id,
            monto=monto,
            fecha_pago=fecha_pago,
            fecha_vencimiento=fecha_vencimiento,
        )
        pago = self.pago_repo.create(db=db, data=pago_data)
        return {"success": True, "pago": pago}

    def obtener_estado_membresia(self, db, cliente_id: int):
        pago_activo = self.pago_repo.get_pago_activo(db, cliente_id)

        if not pago_activo:
            return {"estado": "Vencida", "cliente_id": cliente_id}

        hoy = datetime.now()
        dias_restantes = (pago_activo.fecha_vencimiento - hoy).days

        if dias_restantes <= DIAS_POR_VENCER:
            return {
                "estado": "Por Vencer",
                "cliente_id": cliente_id,
                "dias_restantes": dias_restantes,
                "fecha_vencimiento": pago_activo.fecha_vencimiento.isoformat(),
            }

        return {
            "estado": "Activa",
            "cliente_id": cliente_id,
            "dias_restantes": dias_restantes,
            "fecha_vencimiento": pago_activo.fecha_vencimiento.isoformat(),
        }