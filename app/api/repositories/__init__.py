        return db.query(Usuario).filter(Usuario.cedula == cedula).first()  from app.api.repositories.base_repository import BaseRepository 
from app.api.repositories.reserva_repository import ReservaRepository 
from app.api.repositories.sesion_repository import SesionRepository 
from app.api.repositories.acceso_repository import AccesoRepository 
from app.api.repositories.pago_repository import PagoRepository 
from app.api.repositories.evaluacion_repository import EvaluacionRepository 
from app.api.repositories.plan_repository import PlanRepository 
