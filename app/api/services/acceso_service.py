from app.api.repositories.acceso_repository import AccesoRepository 
from app.api.repositories.pago_repository import PagoRepository 
from app.api.repositories.usuario_repository import UsuarioRepository 
from datetime import datetime 
 
class AccesoService: 
    def __init__(self): 
        self.acceso_repo = AccesoRepository() 
        self.pago_repo = PagoRepository() 
        self.usuario_repo = UsuarioRepository() 
 
    def registrar_entrada(self, cedula: str): 
        usuario = self.usuario_repo.get_by_cedula(cedula) 
        if not usuario: 
            return {"success": False, "error": "ERR_USUARIO_NO_EXISTE", "mensaje": "Usuario no encontrado"} 
 
        if not self.pago_repo.membresia_activa(usuario.id): 
            return {"success": False, "error": "ERR_MEMBRESIA_VENCIDA", "mensaje": "Membresia vencida"} 
 
        acceso = self.acceso_repo.registrar_entrada(usuario.id) 
        return {"success": True, "mensaje": "Acceso registrado", "fecha_hora": acceso.fecha_hora_entrada} 
