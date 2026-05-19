from typing import Optional

from sqlalchemy.orm import Session

from app.api.models.usuario import Usuario


class ClienteRepository:
    """Cliente = usuario del sistema (rol cliente)."""

    @staticmethod
    def get_by_id(db: Session, cliente_id: int) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.idUsuarios == cliente_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()


cliente_repository = ClienteRepository()
