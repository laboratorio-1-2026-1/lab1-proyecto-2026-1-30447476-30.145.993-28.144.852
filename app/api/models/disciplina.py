from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin

class Disciplina(Base, TimestampMixin):
    __tablename__ = "disciplinas"

    idDisciplina = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    duracionMinutos = Column(Integer, nullable=True)

    sesiones = relationship("Sesion", back_populates="disciplina")