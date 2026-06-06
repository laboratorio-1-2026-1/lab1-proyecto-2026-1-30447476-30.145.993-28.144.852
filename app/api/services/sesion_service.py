
from app.api.repositories.sesion_repository import SesionRepository
from datetime import date
from typing import List


class SesionService:
    def __init__(self):
        self.sesion_repo = SesionRepository()

    def crear_sesion(self, db, disciplina, entrenador_id, fecha, hora_inicio, hora_fin, cupo_maximo):
        return self.sesion_repo.create(
            db=db,
            disciplina=disciplina,
            entrenador_id=entrenador_id,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            cupo_maximo=cupo_maximo,
            cupos_disponibles=cupo_maximo,
        )

    def obtener_sesiones_por_fecha(self, db, fecha: date) -> List:
        return self.sesion_repo.get_by_fecha(db, fecha)

    def obtener_sesion(self, db, sesion_id: int):
        return self.sesion_repo.get_by_id(db, sesion_id)


sesion_service = SesionService()