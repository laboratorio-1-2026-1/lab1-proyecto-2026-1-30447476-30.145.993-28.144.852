from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.api.models.base import Base, TimestampMixin

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

    # Relaciones 
    cliente_id = Column(Integer, ForeignKey("usuarios.idUsuarios"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.idUsuarios"), nullable=True)  

    cliente = relationship("Usuario", foreign_keys=[cliente_id], backref="ventas_cliente")
    usuario = relationship("Usuario", foreign_keys=[usuario_id], backref="ventas_usuario")

    # Relación
    ventaDetalles = relationship("VentaDetalle", back_populates="venta", cascade="all, delete-orphan")