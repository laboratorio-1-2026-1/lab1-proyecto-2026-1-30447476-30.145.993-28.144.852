from app.repositories.sesion_repository import SesionRepository 
from datetime import date 
from typing import List 
 
class SesionService: 
    def __init__(self): 
        self.sesion_repo = SesionRepository() 
 
    def crear_sesion(self, disciplina, entrenador_id, fecha, hora_inicio, hora_fin, cupo_maximo): 
        return self.sesion_repo.create( 
            disciplina=disciplina, 
            entrenador_id=entrenador_id, 
            fecha=fecha, 
            hora_inicio=hora_inicio, 
            hora_fin=hora_fin, 
            cupo_maximo=cupo_maximo, 
            cupos_disponibles=cupo_maximo 
        ) 
 
    def obtener_sesiones_por_fecha(self, fecha: date) -
        return self.sesion_repo.get_by_fecha(fecha) 
 
    def obtener_sesion(self, sesion_id: int): 
        return self.sesion_repo.get_by_id(sesion_id) 
