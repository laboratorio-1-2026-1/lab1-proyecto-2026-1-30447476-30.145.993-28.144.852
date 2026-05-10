from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class Sesion(Base):
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, index=True)
    disciplina = Column(String(100), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(DateTime, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    cupo_maximo = Column(Integer, nullable=False)
    cupos_disponibles = Column(Integer, nullable=False)

    # Relaciones
    entrenador = relationship("Usuario", backref="sesiones_dictadas")
    reservas = relationship("Reserva", back_populates="sesion")