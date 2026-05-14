from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.api.models.base import Base, TimestampMixin

class CategoriaProducto(Base):
    __tablename__ = "categoriaProducto"

    idCategoriaProducto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())