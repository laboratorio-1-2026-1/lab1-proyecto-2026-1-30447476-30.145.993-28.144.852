from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.api.repositories.evaluacion_repository import EvaluacionRepository
from app.api.repositories.cliente_repository import ClienteRepository
from app.api.repositories.entrenador_repository import EntrenadorRepository
from app.api.schemas.evaluacion import EvaluacionCreate, EvaluacionUpdate

class EvaluacionService:

    @staticmethod
    def crear(db: Session, data: EvaluacionCreate, usuario_rol: str, usuario_id: int) -> dict:
        # Validar que el cliente existe
        cliente = ClienteRepository.get_by_id(db, data.cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Validar que el entrenador existe
        entrenador = EntrenadorRepository.get_by_id(db, data.entrenador_id)
        if not entrenador:
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    
        evaluacion_data = data.dict()
        if evaluacion_data.get("fechaEvaluacion") is None:
            evaluacion_data["fechaEvaluacion"] = datetime.utcnow()

        evaluacion = EvaluacionRepository.create(db, **evaluacion_data)

        return {
            "status": "success",
            "mensaje": "Evaluación biométrica registrada exitosamente.",
            "data": evaluacion
        }

    @staticmethod
    def listar(
        db: Session,
        skip: int,
        limit: int,
        usuario_rol: str,
        usuario_id: int,
        cliente_id: Optional[int] = None,
        entrenador_id: Optional[int] = None
    ) -> dict:
       
        # Restricciones según rol:
        # - Administrador: puede ver todas las evaluaciones
        # - Entrenador: puede ver las evaluaciones que él mismo ha registrado
        # - Cliente: puede ver solo sus propias evaluaciones
       
        if usuario_rol == "Cliente":
            # Cliente solo ve sus propias evaluaciones
            cliente = ClienteRepository.get_by_usuario_id(db, usuario_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente no encontrado para este usuario")
            cliente_id = cliente.idCliente
        elif usuario_rol == "Entrenador":
            entrenador = EntrenadorRepository.get_by_usuario_id(db, usuario_id)
            if not entrenador:
                raise HTTPException(status_code=404, detail="Entrenador no encontrado para este usuario")
            entrenador_id = entrenador.idEntrenador

        evaluaciones = EvaluacionRepository.get_all(
            db, skip, limit, cliente_id=cliente_id, entrenador_id=entrenador_id
        )
        return {
            "status": "success",
            "mensaje": f"Se encontraron {len(evaluaciones)} evaluaciones.",
            "data": evaluaciones
        }

    @staticmethod
    def obtener(db: Session, evaluacion_id: int, usuario_rol: str, usuario_id: int) -> dict:
        evaluacion = EvaluacionRepository.get_by_id(db, evaluacion_id)
        if not evaluacion:
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")

        # Verificar permisos: cliente solo puede ver su propia evaluación
        if usuario_rol == "Cliente":
            cliente = ClienteRepository.get_by_usuario_id(db, usuario_id)
            if not cliente or cliente.idCliente != evaluacion.cliente_id:
                raise HTTPException(status_code=403, detail="No tiene permiso para ver esta evaluación")
        elif usuario_rol == "Entrenador":
            entrenador = EntrenadorRepository.get_by_usuario_id(db, usuario_id)
            if not entrenador or entrenador.idEntrenador != evaluacion.entrenador_id:
                raise HTTPException(status_code=403, detail="No tiene permiso para ver esta evaluación")
        # Administrador puede ver todo

        return {
            "status": "success",
            "mensaje": "Evaluación encontrada.",
            "data": evaluacion
        }

    @staticmethod
    def actualizar(db: Session, evaluacion_id: int, data: EvaluacionUpdate, usuario_rol: str, usuario_id: int) -> dict:
        evaluacion = EvaluacionRepository.get_by_id(db, evaluacion_id)
        if not evaluacion:
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")

        # Solo Administrador o el entrenador que creó la evaluación pueden actualizarla
        if usuario_rol != "Administrador":
            entrenador = EntrenadorRepository.get_by_usuario_id(db, usuario_id)
            if not entrenador or entrenador.idEntrenador != evaluacion.entrenador_id:
                raise HTTPException(status_code=403, detail="No tiene permiso para modificar esta evaluación")

        evaluacion_actualizada = EvaluacionRepository.update(db, evaluacion_id, **data.dict(exclude_unset=True))
        return {
            "status": "success",
            "mensaje": "Evaluación actualizada exitosamente.",
            "data": evaluacion_actualizada
        }

    @staticmethod
    def eliminar(db: Session, evaluacion_id: int, usuario_rol: str, usuario_id: int) -> dict:
        evaluacion = EvaluacionRepository.get_by_id(db, evaluacion_id)
        if not evaluacion:
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")

        # Solo Administrador o el entrenador que la creó pueden eliminar
        if usuario_rol != "Administrador":
            entrenador = EntrenadorRepository.get_by_usuario_id(db, usuario_id)
            if not entrenador or entrenador.idEntrenador != evaluacion.entrenador_id:
                raise HTTPException(status_code=403, detail="No tiene permiso para eliminar esta evaluación")

        if not EvaluacionRepository.delete(db, evaluacion_id):
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")
        return {
            "status": "success",
            "mensaje": "Evaluación eliminada exitosamente."
        }