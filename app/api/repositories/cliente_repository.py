from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import Cliente
from app.repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):

    def __init__(self):
        super().__init__(Cliente)

    def get_by_cedula(self, db: Session, cedula: str) -> Optional[Cliente]:
        return db.query(Cliente).filter(Cliente.cedula == cedula).first()

    def get_by_usuario_id(self, db: Session, usuario_id: int) -> Optional[Cliente]:
        return db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()

    def get_activos(self, db: Session) -> List[Cliente]:
        return db.query(Cliente).filter(Cliente.activo == True).all()

    def cedula_existe(
        self, db: Session, cedula: str, exclude_id: Optional[int] = None
    ) -> bool:
        q = db.query(Cliente).filter(Cliente.cedula == cedula)
        if exclude_id:
            q = q.filter(Cliente.idClientes != exclude_id)
        return q.first() is not None

    def crear(self, db: Session, datos: dict) -> Cliente:
        cliente = Cliente(**datos)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    def desactivar(self, db: Session, cliente_id: int) -> Optional[Cliente]:
        cliente = self.get_by_id(db, cliente_id)
        if not cliente:
            return None
        cliente.activo = False
        db.commit()
        db.refresh(cliente)
        return cliente


cliente_repository = ClienteRepository()