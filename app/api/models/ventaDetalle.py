from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin

class VentaDetalle(Base, TimestampMixin):
    __tablename__ = "ventasDetalle"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productosTienda.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("ProductoTienda", back_populates="detalles")