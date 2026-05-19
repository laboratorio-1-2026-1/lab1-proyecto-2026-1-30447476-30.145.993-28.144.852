from app.api.repositories.pago_repository import PagoRepository 
from app.api.repositories.plan_repository import PlanRepository 
from datetime import datetime, timedelta 
 
class PagoService: 
    def __init__(self): 
        self.pago_repo = PagoRepository() 
        self.plan_repo = PlanRepository() 
 
    def registrar_pago(self, cliente_id: int, plan_id: int, monto: float): 
        plan = self.plan_repo.get_by_id(plan_id) 
        if not plan: 
            return {"success": False, "mensaje": "Plan no existe"} 
 
        fecha_pago = datetime.now() 
        fecha_vencimiento = fecha_pago + timedelta(days=plan.duracion_dias) 
 
        pago = self.pago_repo.create( 
            cliente_id=cliente_id, 
            plan_id=plan_id, 
            monto=monto, 
            fecha_pago=fecha_pago, 
            fecha_vencimiento=fecha_vencimiento 
        ) 
 
        return {"success": True, "pago": pago} 
 
    def obtener_estado_membresia(self, cliente_id: int): 
        if self.pago_repo.membresia_activa(cliente_id): 
            return {"estado": "Activa", "cliente_id": cliente_id} 
        return {"estado": "Vencida", "cliente_id": cliente_id} 
