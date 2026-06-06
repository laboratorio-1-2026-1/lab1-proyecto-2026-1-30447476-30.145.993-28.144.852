"""
Tests para el módulo de pagos y estado de membresía.
"""
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from app.api.services.pago_service import PagoService


@pytest.fixture
def service():
    return PagoService()


@pytest.fixture
def db():
    return MagicMock()


# ─────────────────────────────────────────────
# registrar_pago
# ─────────────────────────────────────────────

def test_registrar_pago_plan_no_existe(service, db):
    service.plan_repo.get_by_id = MagicMock(return_value=None)

    resultado = service.registrar_pago(db, cliente_id=1, plan_id=99, monto=100.0)

    assert resultado["success"] is False
    assert "Plan no existe" in resultado["mensaje"]


def test_registrar_pago_exitoso(service, db):
    plan_mock = MagicMock()
    plan_mock.duracion_dias = 30
    service.plan_repo.get_by_id = MagicMock(return_value=plan_mock)

    pago_mock = MagicMock()
    service.pago_repo.create = MagicMock(return_value=pago_mock)

    resultado = service.registrar_pago(db, cliente_id=1, plan_id=1, monto=50.0)

    assert resultado["success"] is True
    assert resultado["pago"] == pago_mock


# ─────────────────────────────────────────────
# obtener_estado_membresia
# ─────────────────────────────────────────────

def test_estado_membresia_vencida(service, db):
    service.pago_repo.get_pago_activo = MagicMock(return_value=None)

    resultado = service.obtener_estado_membresia(db, cliente_id=1)

    assert resultado["estado"] == "Vencida"


def test_estado_membresia_activa(service, db):
    pago_mock = MagicMock()
    pago_mock.fecha_vencimiento = datetime.now() + timedelta(days=20)
    service.pago_repo.get_pago_activo = MagicMock(return_value=pago_mock)

    resultado = service.obtener_estado_membresia(db, cliente_id=1)

    assert resultado["estado"] == "Activa"
    assert resultado["dias_restantes"] > 7


def test_estado_membresia_por_vencer(service, db):
    pago_mock = MagicMock()
    pago_mock.fecha_vencimiento = datetime.now() + timedelta(days=3)
    service.pago_repo.get_pago_activo = MagicMock(return_value=pago_mock)

    resultado = service.obtener_estado_membresia(db, cliente_id=1)

    assert resultado["estado"] == "Por Vencer"
    assert resultado["dias_restantes"] <= 7


def test_estado_membresia_por_vencer_exacto(service, db):
    """Membresía que vence exactamente en 7 días → Por Vencer."""
    pago_mock = MagicMock()
    pago_mock.fecha_vencimiento = datetime.now() + timedelta(days=7)
    service.pago_repo.get_pago_activo = MagicMock(return_value=pago_mock)

    resultado = service.obtener_estado_membresia(db, cliente_id=1)

    assert resultado["estado"] == "Por Vencer"