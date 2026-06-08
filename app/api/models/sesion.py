from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin


class Sesion(Base, TimestampMixin):
    __tablename__ = "sesiones"

    id                 = Column(Integer, primary_key=True, index=True)
    disciplina_id      = Column(Integer, ForeignKey("disciplinas.idDisciplina"), nullable=False)
    entrenador_id      = Column(Integer, ForeignKey("entrenadores.idEntrenador"), nullable=False)
    fecha_hora_inicio  = Column(DateTime, nullable=False)
    fecha_hora_fin     = Column(DateTime, nullable=False)
    cupo_maximo        = Column(Integer, nullable=False)
    cupos_disponibles  = Column(Integer, nullable=False)
    ubicacion          = Column(String(100), nullable=True)
    estado             = Column(String(30), default="Programada", nullable=False)

    disciplina = relationship("Disciplina", back_populates="sesiones")
    entrenador = relationship("Entrenador", back_populates="sesiones")
    reservas   = relationship("Reserva", back_populates="sesion")
