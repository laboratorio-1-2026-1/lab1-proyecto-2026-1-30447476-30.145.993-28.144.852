from sqlalchemy import Column, Integer, String, Float
from app.api.core.database import Base   # ← Base compartida

class Plan(Base):
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    duracion_dias = Column(Integer, nullable=False)