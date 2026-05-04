from sqlalchemy import Column, Integer, String, Text, DateTime
from app.models.base import Base

class Rol(Base):
    __tablename__ = "roles"
    
    idRol = Column(Integer, primary_key=True, autoincrement=True)
    nombreRol = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<Rol {self.nombreRol}>"