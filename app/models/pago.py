from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from app.core.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    plan_id = Column(Integer, ForeignKey("planes.id"))
    monto = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)