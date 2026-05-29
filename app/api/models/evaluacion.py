from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.api.models.base import Base, TimestampMixin

class Evaluacion(Base, TimestampMixin):
    __tablename__ = "evaluaciones"

    idEvaluacion = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.idCliente"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("entrenadores.idEntrenador"), nullable=False)
    fechaEvaluacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    peso = Column(Float, nullable=True)
    estatura = Column(Float, nullable=True)
    porcentajeGrasa = Column(Float, nullable=True)
    masaMuscular = Column(Float, nullable=True)
    observaciones = Column(Text, nullable=True)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="evaluaciones")
    entrenador = relationship("Entrenador", back_populates="evaluaciones")