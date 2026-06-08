from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin


class Reserva(Base, TimestampMixin):
    __tablename__ = "reservas"

    id            = Column(Integer, primary_key=True, index=True)
    cliente_id    = Column(Integer, ForeignKey("clientes.idCliente"), nullable=False)
    sesion_id     = Column(Integer, ForeignKey("sesiones.id"), nullable=False)
    fecha_reserva = Column(DateTime, nullable=False)
    estado        = Column(String(50), default="Activa", nullable=False)

    cliente = relationship("Cliente", back_populates="reservas")
    sesion  = relationship("Sesion", back_populates="reservas")
