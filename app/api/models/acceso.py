from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from app.api.database.session import Base


class Acceso(Base):
    __tablename__ = "accesos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.idUsuarios"))
    fecha_hora_entrada = Column(DateTime, nullable=False)
    acceso_permitido = Column(Boolean, default=True, nullable=False)
    mensaje = Column(String(500), nullable=True)
