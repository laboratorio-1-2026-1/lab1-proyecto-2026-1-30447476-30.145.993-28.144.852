from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.api.models.base import Base, TimestampMixin

class EstadoMaquina(str, enum.Enum):
    ACTIVA = "Activa"
    EN_MANTENIMIENTO = "En Mantenimiento"
    FUERA_DE_SERVICIO = "Fuera de Servicio"

class Maquina(Base, TimestampMixin):
    __tablename__ = "maquinas"
    
    idMaquinas = Column(Integer, primary_key=True, autoincrement=True)
    nombreMaquina = Column(String(100), nullable=False)
    descripcionTecnica = Column(Text, nullable=True)
    estadoOperativo = Column(Enum(EstadoMaquina), default=EstadoMaquina.ACTIVA)
    categoria_id = Column(Integer, ForeignKey("categoriasMaquinas.idCategoriasMaquinas"))
    fechaAdquisicion = Column(Date, nullable=True)
    numeroSerie = Column(String(100), unique=True, nullable=True)
    ultimoMantenimiento = Column(Date, nullable=True)
    
    # Relación
    categoria = relationship("CategoriasMaquinas", back_populates="maquinas")
    tickets = relationship("TicketsMantenimiento", back_populates="maquina")
    
    def __repr__(self):
        return f"<Maquina {self.nombreMaquina} - {self.estadoOperativo}>"
