from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models.acceso import Acceso


class AccesoRepository:
    @staticmethod
    def get_todos(db: Session) -> List[Acceso]:
        return db.query(Acceso).order_by(Acceso.fecha_hora_entrada.desc()).all()

    @staticmethod
    def get_por_cliente(db: Session, cliente_id: int) -> List[Acceso]:
        return (
            db.query(Acceso)
            .filter(Acceso.cliente_id == cliente_id)
            .order_by(Acceso.fecha_hora_entrada.desc())
            .all()
        )

    @staticmethod
    def registrar_entrada(
        db: Session,
        cliente_id: int,
        acceso_permitido: bool = True,
        mensaje: str | None = None,
    ) -> Acceso:
        acceso = Acceso(
            cliente_id=cliente_id,
            fecha_hora_entrada=datetime.now(),
            acceso_permitido=acceso_permitido,
            mensaje=mensaje,
        )
        db.add(acceso)
        db.commit()
        db.refresh(acceso)
        return acceso


acceso_repository = AccesoRepository()
