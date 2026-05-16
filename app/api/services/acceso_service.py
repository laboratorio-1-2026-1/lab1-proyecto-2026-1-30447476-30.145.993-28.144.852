from datetime import date
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import ControlAcceso, Cliente
from app.repositories.acceso_repository import acceso_repository
from app.repositories.cliente_repository import cliente_repository


class AccesoService:

    def listar(self, db: Session) -> List[ControlAcceso]:
        return acceso_repository.get_todos(db)

    def listar_por_cliente(self, db: Session, cliente_id: int) -> List[ControlAcceso]:
        return acceso_repository.get_por_cliente(db, cliente_id)

    def registrar_entrada(self, db: Session, cedula: str) -> ControlAcceso:
        """
        Regla de negocio crítica (RF2):
        Recibe la cédula, valida membresía activa y registra el acceso.
        Si la membresía no está vigente → 409 Conflict (acceso denegado).
        El evento se registra en la bitácora SIEMPRE, sea permitido o denegado.
        """
        cliente = cliente_repository.get_by_cedula(db, cedula)

        # Cliente no encontrado — registrar intento y lanzar 409
        if not cliente or not cliente.activo:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_CLIENTE_NO_ENCONTRADO",
                    "mensaje": f"No se encontró un cliente activo con cédula '{cedula}'.",
                },
            )

        membresia = acceso_repository.get_membresia_vigente(db, cliente.idClientes)
        hoy = date.today()

        # Sin membresía
        if not membresia:
            acceso_repository.registrar_entrada(
                db,
                cliente_id=cliente.idClientes,
                membresia_id=None,
                acceso_permitido=False,
                mensaje="El cliente no tiene ninguna membresía registrada.",
            )
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_SIN_MEMBRESIA",
                    "mensaje": "El cliente no tiene ninguna membresía registrada.",
                },
            )

        # Membresía vencida
        if membresia.fechaFin < hoy:
            msg = (
                f"Membresía vencida el {membresia.fechaFin}. "
                "Por favor renueve su plan para acceder al gimnasio."
            )
            acceso_repository.registrar_entrada(
                db,
                cliente_id=cliente.idClientes,
                membresia_id=membresia.idMembresiasClientes,
                acceso_permitido=False,
                mensaje=msg,
            )
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflict",
                    "codigoInterno": "ERR_MEMBRESIA_VENCIDA",
                    "mensaje": msg,
                },
            )

        # Acceso permitido
        msg = f"Acceso permitido. Membresía vigente hasta el {membresia.fechaFin}."
        return acceso_repository.registrar_entrada(
            db,
            cliente_id=cliente.idClientes,
            membresia_id=membresia.idMembresiasClientes,
            acceso_permitido=True,
            mensaje=msg,
        )


acceso_service = AccesoService()