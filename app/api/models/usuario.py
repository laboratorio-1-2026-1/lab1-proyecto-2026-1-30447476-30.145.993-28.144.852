from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin


class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"

    idUsuarios    = Column(Integer, primary_key=True, autoincrement=True)
    nombreUsuario = Column(String(100), unique=True, nullable=False)
    email         = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    activo        = Column(Boolean, default=True, nullable=False)
    rol_id        = Column(Integer, ForeignKey("roles.idRol"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")

    def __repr__(self):
        return f"<Usuario {self.email}>"