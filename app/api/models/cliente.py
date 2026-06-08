from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.api.models.base import Base, TimestampMixin


class Cliente(Base, TimestampMixin):
    __tablename__ = "clientes"

    idCliente       = Column(Integer, primary_key=True, index=True)
    usuario_id      = Column(Integer, ForeignKey("usuarios.idUsuarios"), nullable=True)
    nombre          = Column(String(100), nullable=False)
    apellido        = Column(String(100), nullable=False)
    cedula          = Column(String(20), unique=True, nullable=False, index=True)
    telefono        = Column(String(20), nullable=True)
    fechaNacimiento = Column(Date, nullable=True)
    fechaRegistro   = Column(DateTime, default=datetime.utcnow)
    activo          = Column(Boolean, default=True)

    usuario      = relationship("Usuario", back_populates="clientes")
    reservas     = relationship("Reserva", back_populates="cliente")
    accesos      = relationship("Acceso", back_populates="cliente")
    evaluaciones = relationship("Evaluacion", back_populates="cliente")
    pagos        = relationship("Pago", back_populates="cliente")
    ventas       = relationship("Venta", back_populates="cliente", foreign_keys="[Venta.cliente_id]")
