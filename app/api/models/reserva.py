from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.api.database.session import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.idUsuarios"))
    sesion_id = Column(Integer, ForeignKey("sesiones.id"))
    fecha_reserva = Column(DateTime, nullable=False)
    estado = Column(String(50), default="Activa", nullable=False)

    cliente = relationship("Usuario", backref="mis_reservas")
    sesion = relationship("Sesion", back_populates="reservas")
