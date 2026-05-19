from app.api.repositories.evaluacion_repository import EvaluacionRepository 
from datetime import datetime 
 
class EvaluacionService: 
    def __init__(self): 
        self.evaluacion_repo = EvaluacionRepository() 
 
    def registrar_evaluacion(self, cliente_id: int, entrenador_id: int, peso: float, estatura: float, grasa_corporal: float = None, observaciones: str = None): 
        return self.evaluacion_repo.create( 
            cliente_id=cliente_id, 
            entrenador_id=entrenador_id, 
            peso=peso, 
            estatura=estatura, 
            grasa_corporal=grasa_corporal, 
            observaciones=observaciones, 
            fecha=datetime.now() 
        ) 
 
    def obtener_historial_cliente(self, cliente_id: int): 
        return self.evaluacion_repo.get_by_cliente(cliente_id) 
