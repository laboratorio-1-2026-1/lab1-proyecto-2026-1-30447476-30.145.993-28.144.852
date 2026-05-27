from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.api.repositories.disciplina_repository import DisciplinaRepository
from app.api.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate

class DisciplinaService:

    @staticmethod
    def crear(db: Session, data: DisciplinaCreate) -> dict:
        if DisciplinaRepository.get_by_nombre(db, data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_NOMBRE_DUPLICADO",
                    "mensaje": f"Ya existe una disciplina con el nombre '{data.nombre}'.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        disciplina = DisciplinaRepository.create(db, **data.dict())
        return {
            "status": "success",
            "mensaje": "Disciplina creada exitosamente.",
            "data": disciplina
        }

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100) -> dict:
        disciplinas = DisciplinaRepository.get_all(db, skip, limit)
        return {
            "status": "success",
            "mensaje": f"Se encontraron {len(disciplinas)} disciplinas.",
            "data": disciplinas
        }

    @staticmethod
    def obtener(db: Session, disciplina_id: int) -> dict:
        disciplina = DisciplinaRepository.get_by_id(db, disciplina_id)
        if not disciplina:
            raise HTTPException(status_code=404, detail="Disciplina no encontrada")
        return {
            "status": "success",
            "mensaje": "Disciplina encontrada.",
            "data": disciplina
        }

    @staticmethod
    def actualizar(db: Session, disciplina_id: int, data: DisciplinaUpdate) -> dict:
        disciplina_actual = DisciplinaRepository.get_by_id(db, disciplina_id)
        if not disciplina_actual:
            raise HTTPException(status_code=404, detail="Disciplina no encontrada")
        # Si se cambia el nombre, verificar unicidad
        if data.nombre and data.nombre != disciplina_actual.nombre:
            if DisciplinaRepository.get_by_nombre(db, data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "error": "Conflict",
                        "codigoInterno": "ERR_NOMBRE_DUPLICADO",
                        "mensaje": f"Ya existe otra disciplina con el nombre '{data.nombre}'.",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
        disciplina_actualizada = DisciplinaRepository.update(db, disciplina_id, **data.dict(exclude_unset=True))
        return {
            "status": "success",
            "mensaje": "Disciplina actualizada exitosamente.",
            "data": disciplina_actualizada
        }

    @staticmethod
    def eliminar(db: Session, disciplina_id: int) -> dict:
        if not DisciplinaRepository.delete(db, disciplina_id):
            raise HTTPException(status_code=404, detail="Disciplina no encontrada")
        return {
            "status": "success",
            "mensaje": "Disciplina eliminada exitosamente."
        }