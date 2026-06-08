from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin


class Acceso(Base, TimestampMixin):
    __tablename__ = "accesos"

    id                 = Column(Integer, primary_key=True, index=True)
    cliente_id         = Column(Integer, ForeignKey("clientes.idCliente"), nullable=False)
    fecha_hora_entrada = Column(DateTime, nullable=False)
    acceso_permitido   = Column(Boolean, default=True, nullable=False)
    mensaje            = Column(String(500), nullable=True)

    cliente = relationship("Cliente", back_populates="accesos")
