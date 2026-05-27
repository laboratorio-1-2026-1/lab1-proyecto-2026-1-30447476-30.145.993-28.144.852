from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.api.repositories.entrenador_repository import EntrenadorRepository
from app.api.schemas.entrenador import EntrenadorCreate, EntrenadorUpdate

class EntrenadorService:

    @staticmethod
    def crear(db: Session, data: EntrenadorCreate, usuario_id: int = None) -> dict:
        # Validar cédula única
        if EntrenadorRepository.get_by_cedula(db, data.cedula):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_CEDULA_DUPLICADA",
                    "mensaje": f"Ya existe un entrenador con la cédula '{data.cedula}'.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        # Validar correo único 
        if data.correo and EntrenadorRepository.get_by_correo(db, data.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_CORREO_DUPLICADO",
                    "mensaje": f"Ya existe un entrenador con el correo '{data.correo}'.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        entrenador_data = data.dict()
        if usuario_id:
            entrenador_data["usuario_id"] = usuario_id
        entrenador = EntrenadorRepository.create(db, **entrenador_data)
        return {
            "status": "success",
            "mensaje": "Entrenador registrado exitosamente.",
            "data": entrenador
        }

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100, solo_activos: bool = True) -> dict:
        entrenadores = EntrenadorRepository.get_all(db, skip, limit, solo_activos)
        return {
            "status": "success",
            "mensaje": f"Se encontraron {len(entrenadores)} entrenadores.",
            "data": entrenadores
        }

    @staticmethod
    def obtener(db: Session, entrenador_id: int) -> dict:
        entrenador = EntrenadorRepository.get_by_id(db, entrenador_id)
        if not entrenador:
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")
        return {
            "status": "success",
            "mensaje": "Entrenador encontrado.",
            "data": entrenador
        }

    @staticmethod
    def actualizar(db: Session, entrenador_id: int, data: EntrenadorUpdate) -> dict:
        entrenador_actual = EntrenadorRepository.get_by_id(db, entrenador_id)
        if not entrenador_actual:
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")
        # Validar cédula si se cambia
        if data.cedula and data.cedula != entrenador_actual.cedula:
            if EntrenadorRepository.get_by_cedula(db, data.cedula):
                raise HTTPException(status_code=409, detail="Cédula ya registrada")
        # Validar correo si se cambia
        if data.correo and data.correo != entrenador_actual.correo:
            if EntrenadorRepository.get_by_correo(db, data.correo):
                raise HTTPException(status_code=409, detail="Correo ya registrado")
        entrenador_actualizado = EntrenadorRepository.update(db, entrenador_id, **data.dict(exclude_unset=True))
        return {
            "status": "success",
            "mensaje": "Entrenador actualizado exitosamente.",
            "data": entrenador_actualizado
        }

    @staticmethod
    def eliminar(db: Session, entrenador_id: int) -> dict:
        if not EntrenadorRepository.delete(db, entrenador_id):
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")
        return {
            "status": "success",
            "mensaje": "Entrenador desactivado exitosamente."
        }