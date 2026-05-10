from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    sesion_id = Column(Integer, ForeignKey("sesiones.id"))
    fecha_reserva = Column(DateTime, nullable=False)

    # Relaciones
    cliente = relationship("Usuario", backref="mis_reservas")
    sesion = relationship("Sesion", back_populates="reservas")