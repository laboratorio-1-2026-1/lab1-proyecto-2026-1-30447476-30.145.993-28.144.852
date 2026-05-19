from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from app.api.core.database import Base   # ← Base compartida

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.idUsuarios"))
    entrenador_id = Column(Integer, ForeignKey("usuarios.idUsuarios"))
    peso = Column(Float)
    estatura = Column(Float)
    grasa_corporal = Column(Float)
    observaciones = Column(String(500))
    fecha = Column(DateTime, nullable=False)