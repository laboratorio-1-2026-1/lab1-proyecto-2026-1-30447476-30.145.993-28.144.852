from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin

class Entrenador(Base, TimestampMixin):
    __tablename__ = "entrenadores"

    idEntrenador = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.idUsuario"), nullable=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(255), unique=True, nullable=True)
    especialidad = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    usuario = relationship("Usuario", backref="entrenador")
    sesiones = relationship("Sesion", back_populates="entrenador")
    evaluaciones = relationship("EvaluacionBiometrica", back_populates="entrenador")
