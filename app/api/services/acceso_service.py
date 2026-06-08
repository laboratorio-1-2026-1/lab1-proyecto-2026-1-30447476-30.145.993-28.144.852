from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.models.acceso import Acceso
from app.api.repositories.acceso_repository import AccesoRepository
from app.api.repositories.cliente_repository import ClienteRepository
from app.api.repositories.pago_repository import PagoRepository


class AccesoService:
    def listar(self, db: Session) -> List[Acceso]:
        return AccesoRepository.get_todos(db)

    def listar_por_cliente(self, db: Session, cliente_id: int) -> List[Acceso]:
        return AccesoRepository.get_por_cliente(db, cliente_id)

    def registrar_entrada(self, db: Session, cedula: str):
        cliente = ClienteRepository.get_by_cedula(db, cedula)
        if not cliente:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_ACCESO_CLIENTE_NO_ENCONTRADO",
                    "mensaje": f"No existe ningún cliente con la cédula '{cedula}'.",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

        if not cliente.activo:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_ACCESO_CLIENTE_INACTIVO",
                    "mensaje": "El cliente está inactivo en el sistema.",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

        if not PagoRepository.membresia_activa(db, cliente.idCliente):
            AccesoRepository.registrar_entrada(
                db,
                cliente_id=cliente.idCliente,
                acceso_permitido=False,
                mensaje="Acceso denegado: membresía vencida o inexistente.",
            )
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_ACCESO_MEMBRESIA_INACTIVA",
                    "mensaje": "Acceso denegado: el cliente no tiene una membresía pagada y vigente.",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

        return AccesoRepository.registrar_entrada(
            db,
            cliente_id=cliente.idCliente,
            acceso_permitido=True,
            mensaje="Acceso permitido.",
        )


acceso_service = AccesoService()
