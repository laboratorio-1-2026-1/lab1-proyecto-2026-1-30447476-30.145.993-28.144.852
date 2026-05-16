from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship 
import enum
from app.api.models.base import Base, TimestampMixin
from app.api.models.ventaDetalle import VentaDetalle

class EstadoVenta(str, enum.Enum):
    COMPLETADA = "COMPLETADA"
    DEVUELTA = "DEVUELTA"
    CANCELADA = "CANCELADA"


class Venta(Base, TimestampMixin):
    __tablename__ = "ventas"
    
    idVenta = Column(Integer, primary_key=True, index=True)
    numeroVenta = Column(String(50), unique=True, nullable=False)
    fechaVenta = Column(DateTime, nullable=False)
    montoTotal = Column(Float, nullable=False)
    metodoPago = Column(String(50))
    estado = Column(Enum(EstadoVenta), default=EstadoVenta.COMPLETADA)
   
    # Relación con cliente
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    cliente = relationship("Cliente", back_populates="ventas") 

    # Relación con los detalles de venta
    ventaDetalles = relationship(
        "VentaDetalle", 
        back_populates="venta", 
        cascade="all, delete-orphan"
    )