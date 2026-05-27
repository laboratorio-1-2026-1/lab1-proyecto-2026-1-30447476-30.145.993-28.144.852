from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.api.repositories.cliente_repository import ClienteRepository
from app.api.schemas.cliente import ClienteCreate, ClienteUpdate

class ClienteService:
    @staticmethod
    def crear(db: Session, data: ClienteCreate, usuario_id: int = None):
        # Validar cédula única
        if ClienteRepository.get_by_cedula(db, data.cedula):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_CEDULA_DUPLICADA",
                    "mensaje": f"Ya existe un cliente con la cédula '{data.cedula}'.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        cliente_data = data.dict()
        if usuario_id:
            cliente_data["usuario_id"] = usuario_id
        cliente = ClienteRepository.create(db, **cliente_data)
        return {
            "status": "success",
            "mensaje": "Cliente registrado exitosamente.",
            "data": cliente
        }

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100):
        clientes = ClienteRepository.get_all(db, skip, limit)
        return {
            "status": "success",
            "mensaje": f"Se encontraron {len(clientes)} clientes.",
            "data": clientes
        }

    @staticmethod
    def obtener(db: Session, cliente_id: int):
        cliente = ClienteRepository.get_by_id(db, cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {
            "status": "success",
            "mensaje": "Cliente encontrado.",
            "data": cliente
        }

    @staticmethod
    def actualizar(db: Session, cliente_id: int, data: ClienteUpdate):
        cliente = ClienteRepository.get_by_id(db, cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        # Si se cambia cédula, verificar unicidad
        if data.cedula and data.cedula != cliente.cedula:
            if ClienteRepository.get_by_cedula(db, data.cedula):
                raise HTTPException(status_code=409, detail="Cédula ya registrada")
        cliente_actualizado = ClienteRepository.update(db, cliente_id, **data.dict(exclude_unset=True))
        return {
            "status": "success",
            "mensaje": "Cliente actualizado exitosamente.",
            "data": cliente_actualizado
        }

    @staticmethod
    def eliminar(db: Session, cliente_id: int):
        if not ClienteRepository.delete(db, cliente_id):
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {"status": "success", "mensaje": "Cliente eliminado"}