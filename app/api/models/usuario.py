from sqlalchemy import Column, Integer, String, Enum
from app.api.core.database import Base
import enum

class RolEnum(str, enum.Enum):
    ADMIN = "Administracion"
    FINANZAS = "Finanzas"
    ENTRENADOR = "Entrenador"
    CLIENTE = "Cliente"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.CLIENTE)