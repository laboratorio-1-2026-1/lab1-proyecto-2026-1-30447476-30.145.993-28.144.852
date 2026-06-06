"""
Tests para el módulo de reservas.
"""
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.api.services.reserva_service import ReservaService


@pytest.fixture
def service():
    return ReservaService()


@pytest.fixture
def db():
    return MagicMock()


def _make_sesion(estado="Programada", cupos=5):
    sesion = MagicMock()
    sesion.estado = estado
    sesion.cupos_disponibles = cupos
    return sesion


def _make_cliente(activo=True):
    cliente = MagicMock()
    cliente.activo = activo
    return cliente


# ─────────────────────────────────────────────
# crear reserva
# ─────────────────────────────────────────────

def test_crear_reserva_cliente_inactivo(service, db):
    with patch("app.api.services.reserva_service.ClienteRepository") as mock_cr, \
         patch("app.api.services.reserva_service.sesion_repository"):
        mock_cr.get_by_id.return_value = _make_cliente(activo=False)

        with pytest.raises(HTTPException) as exc:
            service.crear(db, cliente_id=1, sesion_id=1)

        assert exc.value.status_code == 404


def test_crear_reserva_sesion_no_encontrada(service, db):
    with patch("app.api.services.reserva_service.ClienteRepository") as mock_cr, \
         patch("app.api.services.reserva_service.sesion_repository") as mock_sr:
        mock_cr.get_by_id.return_value = _make_cliente()
        mock_sr.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc:
            service.crear(db, cliente_id=1, sesion_id=99)

        assert exc.value.status_code == 404


def test_crear_reserva_sesion_no_programada(service, db):
    with patch("app.api.services.reserva_service.ClienteRepository") as mock_cr, \
         patch("app.api.services.reserva_service.sesion_repository") as mock_sr:
        mock_cr.get_by_id.return_value = _make_cliente()
        mock_sr.get_by_id.return_value = _make_sesion(estado="Cancelada")

        with pytest.raises(HTTPException) as exc:
            service.crear(db, cliente_id=1, sesion_id=1)

        assert exc.value.status_code == 409
        assert exc.value.detail["codigoInterno"] == "ERR_RESERVA_SESION_NO_DISPONIBLE"


def test_crear_reserva_duplicada(service, db):
    with patch("app.api.services.reserva_service.ClienteRepository") as mock_cr, \
         patch("app.api.services.reserva_service.sesion_repository") as mock_sr, \
         patch("app.api.services.reserva_service.reserva_repository") as mock_rr:
        mock_cr.get_by_id.return_value = _make_cliente()
        mock_sr.get_by_id.return_value = _make_sesion()
        mock_rr.existe_reserva_activa.return_value = True

        with pytest.raises(HTTPException) as exc:
            service.crear(db, cliente_id=1, sesion_id=1)

        assert exc.value.status_code == 409
        assert exc.value.detail["codigoInterno"] == "ERR_RESERVA_DUPLICADA"


def test_crear_reserva_sin_cupos(service, db):
    with patch("app.api.services.reserva_service.ClienteRepository") as mock_cr, \
         patch("app.api.services.reserva_service.sesion_repository") as mock_sr, \
         patch("app.api.services.reserva_service.reserva_repository") as mock_rr:
        mock_cr.get_by_id.return_value = _make_cliente()
        mock_sr.get_by_id.return_value = _make_sesion(cupos=0)
        mock_rr.existe_reserva_activa.return_value = False

        with pytest.raises(HTTPException) as exc:
            service.crear(db, cliente_id=1, sesion_id=1)

        assert exc.value.status_code == 409
        assert exc.value.detail["codigoInterno"] == "ERR_RESERVA_SIN_CUPOS"


def test_crear_reserva_solapamiento(service, db):
    with patch("app.api.services.reserva_service.ClienteRepository") as mock_cr, \
         patch("app.api.services.reserva_service.sesion_repository") as mock_sr, \
         patch("app.api.services.reserva_service.reserva_repository") as mock_rr:
        mock_cr.get_by_id.return_value = _make_cliente()
        mock_sr.get_by_id.return_value = _make_sesion()
        mock_rr.existe_reserva_activa.return_value = False
        mock_rr.hay_solapamiento.return_value = True

        with pytest.raises(HTTPException) as exc:
            service.crear(db, cliente_id=1, sesion_id=1)

        assert exc.value.status_code == 409
        assert exc.value.detail["codigoInterno"] == "ERR_RESERVA_SOLAPAMIENTO"


def test_crear_reserva_exitosa(service, db):
    with patch("app.api.services.reserva_service.ClienteRepository") as mock_cr, \
         patch("app.api.services.reserva_service.sesion_repository") as mock_sr, \
         patch("app.api.services.reserva_service.reserva_repository") as mock_rr:
        mock_cr.get_by_id.return_value = _make_cliente()
        mock_sr.get_by_id.return_value = _make_sesion()
        mock_rr.existe_reserva_activa.return_value = False
        mock_rr.hay_solapamiento.return_value = False
        reserva_mock = MagicMock()
        mock_rr.crear.return_value = reserva_mock

        resultado = service.crear(db, cliente_id=1, sesion_id=1)

        assert resultado == reserva_mock


# ─────────────────────────────────────────────
# cancelar reserva
# ─────────────────────────────────────────────

def test_cancelar_reserva_ya_cancelada(service, db):
    with patch("app.api.services.reserva_service.reserva_repository") as mock_rr:
        reserva_mock = MagicMock()
        reserva_mock.estado = "Cancelada"
        mock_rr.get_by_id.return_value = reserva_mock

        with pytest.raises(HTTPException) as exc:
            service.cancelar(db, reserva_id=1)

        assert exc.value.status_code == 409
        assert exc.value.detail["codigoInterno"] == "ERR_RESERVA_YA_CANCELADA"


def test_cancelar_reserva_exitosa(service, db):
    with patch("app.api.services.reserva_service.reserva_repository") as mock_rr:
        reserva_mock = MagicMock()
        reserva_mock.estado = "Activa"
        mock_rr.get_by_id.return_value = reserva_mock
        cancelada_mock = MagicMock()
        mock_rr.cancelar.return_value = cancelada_mock

        resultado = service.cancelar(db, reserva_id=1)

        assert resultado == cancelada_mock
        