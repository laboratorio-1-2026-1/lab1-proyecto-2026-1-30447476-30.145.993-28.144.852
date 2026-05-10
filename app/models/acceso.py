from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.core.database import Base

class Acceso(Base):
    __tablename__ = "accesos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_hora_entrada = Column(DateTime, nullable=False)