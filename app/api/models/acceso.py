from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.api.core.database import Base   # ← Base compartida

class Acceso(Base):
    __tablename__ = "accesos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.idUsuarios"))
    fecha_hora_entrada = Column(DateTime, nullable=False)