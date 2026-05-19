from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin

class ProductoTienda(Base, TimestampMixin):
    __tablename__ = "productosTienda"   

    idProductosTienda = Column(Integer, primary_key=True, index=True)  
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(String(500), nullable=True)    # text
    categoriaProducto_id = Column(Integer, ForeignKey("categoriaProducto.idCategoriaProducto"), nullable=False)
    precio = Column(Float, nullable=False)              
    stock = Column(Integer, default=0, nullable=False)
    codigoBarra = Column(String(50), unique=True, nullable=True)  
    activo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación (opcional)
    categoria = relationship("CategoriaProducto", backref="productos")
    ventaDetalles = relationship("VentaDetalle", back_populates="producto")
