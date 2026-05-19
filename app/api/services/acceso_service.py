from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.models.acceso import Acceso
from app.api.repositories.acceso_repository import acceso_repository
from app.api.repositories.cliente_repository import cliente_repository


class AccesoService:
    def listar(self, db: Session) -> List[Acceso]:
        return acceso_repository.get_todos(db)

    def listar_por_cliente(self, db: Session, cliente_id: int) -> List[Acceso]:
        return acceso_repository.get_por_cliente(db, cliente_id)

    def registrar_entrada(self, db: Session, email: str) -> Acceso:
        cliente = cliente_repository.get_by_email(db, email)
        if not cliente or not cliente.activo:
            raise HTTPException(
                status_code=409,
                detail="Cliente no encontrado o inactivo.",
            )

        return acceso_repository.registrar_entrada(
            db,
            cliente_id=cliente.idUsuarios,
            acceso_permitido=True,
            mensaje="Acceso permitido.",
        )


acceso_service = AccesoService()
