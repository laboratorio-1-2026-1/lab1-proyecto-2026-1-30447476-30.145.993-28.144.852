from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin

class VentaDetalle(Base, TimestampMixin):
    __tablename__ = "ventasDetalle"

    idVentaDetalles = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.idVenta"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productosTienda.idProductosTienda"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precioUnitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    

    # Relaciones
    venta = relationship("Venta", back_populates="ventaDetalles")
    producto = relationship("ProductoTienda", back_populates="ventaDetalles")