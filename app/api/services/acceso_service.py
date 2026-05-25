from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.models.acceso import Acceso
from app.api.repositories.acceso_repository import acceso_repository
from app.api.repositories.cliente_repository import cliente_repository
from app.api.repositories.pago_repository import PagoRepository


class AccesoService:
    def listar(self, db: Session) -> List[Acceso]:
        return acceso_repository.get_todos(db)

    def listar_por_cliente(self, db: Session, cliente_id: int) -> List[Acceso]:
        return acceso_repository.get_por_cliente(db, cliente_id)

    def registrar_entrada(self, db: Session, cedula: str):
        """
        REGLA CRÍTICA: Valida cédula y membresía vigente antes de permitir acceso.
        Retorna 409 Conflict si el cliente no tiene membresía activa.
        """
        # 1. Buscar cliente por cédula (no por email)
        cliente = cliente_repository.get_by_cedula(db, cedula)
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

        # 2. REGLA CRÍTICA: Verificar membresía activa
        pago_repo = PagoRepository()
        if not pago_repo.membresia_activa(db, cliente.idUsuarios):
            acceso_repository.registrar_entrada(
                db,
                cliente_id=cliente.idUsuarios,
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

        # 3. Membresía válida → registrar entrada exitosa
        return acceso_repository.registrar_entrada(
            db,
            cliente_id=cliente.idUsuarios,
            acceso_permitido=True,
            mensaje="Acceso permitido.",
        )


acceso_service = AccesoService()