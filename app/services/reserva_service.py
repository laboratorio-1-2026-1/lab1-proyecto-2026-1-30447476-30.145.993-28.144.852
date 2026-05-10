from app.repositories.sesion_repository import SesionRepository 
from datetime import datetime 
 
class ReservaService: 
    def __init__(self): 
        self.reserva_repo = ReservaRepository() 
        self.sesion_repo = SesionRepository() 
 
    def crear_reserva(self, cliente_id: int, sesion_id: int): 
        sesion = self.sesion_repo.get_by_id(sesion_id) 
        if not sesion: 
            return {"success": False, "error": "ERR_SESION_NO_EXISTE", "mensaje": "La sesion no existe"} 
 
            return {"success": False, "error": "ERR_CUPO_AGOTADO", "mensaje": "No hay cupos disponibles"} 
 
        reserva = self.reserva_repo.create( 
            cliente_id=cliente_id, 
            sesion_id=sesion_id, 
            fecha_reserva=datetime.now() 
        ) 
 
        nuevo_cupo = sesion.cupos_disponibles - 1 
        self.sesion_repo.update(sesion_id, cupos_disponibles=nuevo_cupo) 
 
        return {"success": True, "reserva": reserva, "cupos_restantes": nuevo_cupo} 
 
    def cancelar_reserva(self, reserva_id: int, cliente_id: int): 
        reserva = self.reserva_repo.get_by_id(reserva_id) 
        if not reserva: 
            return {"success": False, "mensaje": "La reserva no existe"} 
 
        if reserva.cliente_id != cliente_id: 
            return {"success": False, "mensaje": "No puedes cancelar reservas de otro cliente"} 
 
        sesion = self.sesion_repo.get_by_id(reserva.sesion_id) 
        if sesion: 
            nuevo_cupo = sesion.cupos_disponibles + 1 
            self.sesion_repo.update(sesion.id, cupos_disponibles=nuevo_cupo) 
 
        self.reserva_repo.delete(reserva_id) 
        return {"success": True, "mensaje": "Reserva cancelada exitosamente"} 
 
    def obtener_reservas_cliente(self, cliente_id: int): 
        return self.reserva_repo.get_by_cliente(cliente_id) 
