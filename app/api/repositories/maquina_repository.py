from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.models.maquina import Maquina
from app.api.models.categoriasMaquinas import CategoriasMaquinas
from app.api.schemas.maquina import MaquinaCreate, MaquinaUpdate


class MaquinaRepository:

    @staticmethod
    def get_all(
        db: Session,
        categoria_id: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[Maquina]:
        q = db.query(Maquina)
        if categoria_id is not None:
            q = q.filter(Maquina.categoria_id == categoria_id)
        if estado is not None:
            q = q.filter(Maquina.estadoOperativo == estado)
        return q.order_by(Maquina.idMaquinas).all()

    @staticmethod
    def get_by_id(db: Session, maquina_id: int) -> Optional[Maquina]:
        return db.query(Maquina).filter(Maquina.idMaquinas == maquina_id).first()

    @staticmethod
    def get_by_numeroSerie(db: Session, numeroSerie: str) -> Optional[Maquina]:
        return db.query(Maquina).filter(Maquina.numeroSerie == numeroSerie).first()

    @staticmethod
    def create(db: Session, data: MaquinaCreate) -> Maquina:
        maquina = Maquina(
            nombreMaquina=data.nombreMaquina,
            descripcionTecnica=data.descripcionTecnica,
            categoria_id=data.categoria_id,
            fechaAdquisicion=data.fechaAdquisicion,
            numeroSerie=data.numeroSerie,
        )
        db.add(maquina)
        db.commit()
        db.refresh(maquina)
        return maquina

    @staticmethod
    def update(db: Session, maquina_id: int, data: MaquinaUpdate) -> Optional[Maquina]:
        maquina = MaquinaRepository.get_by_id(db, maquina_id)
        if not maquina:
            return None
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(maquina, field, value)
        db.commit()
        db.refresh(maquina)
        return maquina

    @staticmethod
    def update_estado(db: Session, maquina_id: int, nuevoEstado: str) -> Optional[Maquina]:
        maquina = MaquinaRepository.get_by_id(db, maquina_id)
        if not maquina:
            return None
        maquina.estadoOperativo = nuevoEstado
        db.commit()
        db.refresh(maquina)
        return maquina

    @staticmethod
    def delete(db: Session, maquina_id: int) -> bool:
        maquina = MaquinaRepository.get_by_id(db, maquina_id)
        if not maquina:
            return False
        db.delete(maquina)
        db.commit()
        return True

    # ── Categorías ────────────────────────────────────────────────────────────

    @staticmethod
    def get_all_categorias(db: Session) -> List[CategoriasMaquinas]:
        return db.query(CategoriasMaquinas).order_by(CategoriasMaquinas.idCategoriasMaquinas).all()

    @staticmethod
    def get_categoria_by_id(db: Session, categoria_id: int) -> Optional[CategoriasMaquinas]:
        return db.query(CategoriasMaquinas).filter(
            CategoriasMaquinas.idCategoriasMaquinas == categoria_id
        ).first()

    @staticmethod
    def create_categoria(
        db: Session, nombre: str, descripcion: Optional[str] = None
    ) -> CategoriasMaquinas:
        categoria = CategoriasMaquinas(nombre=nombre, descripcion=descripcion)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return categoria 