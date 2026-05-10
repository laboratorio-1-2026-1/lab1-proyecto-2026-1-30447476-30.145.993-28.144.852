from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from app.core.database import Base

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    entrenador_id = Column(Integer, ForeignKey("usuarios.id"))
    peso = Column(Float)
    estatura = Column(Float)
    grasa_corporal = Column(Float)
    observaciones = Column(String(500))
    fecha = Column(DateTime, nullable=False)