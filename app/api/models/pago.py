from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from app.api.core.database import Base   # ← Base compartida

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.idUsuarios"))
    plan_id = Column(Integer, ForeignKey("planes.id"))
    monto = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)