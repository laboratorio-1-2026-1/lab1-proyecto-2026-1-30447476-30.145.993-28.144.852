from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"
    
    idUsuarios = Column(Integer, primary_key=True, autoincrement=True)
    nombreUsuario = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("roles.idRol"), nullable=False)
    
    # Relaciones
    rol = relationship("Rol", backref="usuarios")
    cliente = relationship("Cliente", uselist=False, back_populates="usuario")
    
    def __repr__(self):
        return f"<Usuario {self.email}>"