from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String, event
from sqlalchemy.orm import relationship
from app.api.database.session import Base
from datetime import datetime


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.idUsuarios"), nullable=False)
    plan_id = Column(Integer, ForeignKey("planes.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=False)
    nombre_plan_snapshot = Column(String(100), nullable=True)
    precio_plan_snapshot = Column(Float, nullable=True)
    metodo_pago = Column(String(50), nullable=True)
    referencia = Column(String(100), nullable=True)
    descripcion = Column(String(255), nullable=True)

    cliente = relationship("Usuario", foreign_keys=[cliente_id])
    plan = relationship("Plan", foreign_keys=[plan_id])


@event.listens_for(Pago, "before_update")
def bloquear_update_pago(mapper, connection, target):
    raise ValueError("ERR_PAGO_INMUTABLE: Los registros de pago no pueden modificarse.")


@event.listens_for(Pago, "before_delete")
def bloquear_delete_pago(mapper, connection, target):
    raise ValueError("ERR_PAGO_INMUTABLE: Los registros de pago no pueden eliminarse.")
