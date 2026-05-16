from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.api.models.base import Base, TimestampMixin


class Rol(Base, TimestampMixin):
    __tablename__ = "roles"

    idRol       = Column(Integer, primary_key=True, autoincrement=True)
    nombreRol   = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        return f"<Rol {self.nombreRol}>"