import pytest
from tests.conftest import crear_rol, crear_usuario, crear_plan, crear_pago


@pytest.fixture()
def datos_acceso(db):
    rol_admin   = crear_rol(db, "Administrador")
    rol_cliente = crear_rol(db, "Cliente")
    plan = crear_plan(db, "Plan Básico", 25.0, 30)

    cliente_activo = crear_usuario(
        db, "cli_activo", "activo@gym.com", "pass1234",
        rol_id=rol_cliente.idRol, cedula="V-11111111",
    )
    crear_pago(db, cliente_activo.idUsuarios, plan.id, 25.0, dias_offset=20)

    cliente_vencido = crear_usuario(
        db, "cli_vencido", "vencido@gym.com", "pass1234",
        rol_id=rol_cliente.idRol, cedula="V-22222222",
    )
    crear_pago(db, cliente_vencido.idUsuarios, plan.id, 25.0, dias_offset=-5)

    cliente_sin_pago = crear_usuario(
        db, "cli_sinpago", "sinpago@gym.com", "pass1234",
        rol_id=rol_cliente.idRol, cedula="V-33333333",
    )
    return {
        "cliente_activo":   cliente_activo,
        "cliente_vencido":  cliente_vencido,
        "cliente_sin_pago": cliente_sin_pago,
    }


def test_acceso_permitido_con_membresia_activa(client, datos_acceso):
    resp = client.post("/api/v1/accesos/entrada",
                       json={"documento_identidad": "V-11111111"})
    assert resp.status_code == 200
    assert resp.json()["acceso_permitido"] is True


def test_acceso_denegado_membresia_vencida(client, datos_acceso):
    resp = client.post("/api/v1/accesos/entrada",
                       json={"documento_identidad": "V-22222222"})
    assert resp.status_code == 409
    assert resp.json()["detail"]["codigoInterno"] == "ERR_ACCESO_MEMBRESIA_INACTIVA"


def test_acceso_denegado_sin_pago(client, datos_acceso):
    resp = client.post("/api/v1/accesos/entrada",
                       json={"documento_identidad": "V-33333333"})
    assert resp.status_code == 409
    assert resp.json()["detail"]["codigoInterno"] == "ERR_ACCESO_MEMBRESIA_INACTIVA"


def test_acceso_cedula_inexistente(client, datos_acceso):
    resp = client.post("/api/v1/accesos/entrada",
                       json={"documento_identidad": "V-00000000"})
    assert resp.status_code == 409
    assert resp.json()["detail"]["codigoInterno"] == "ERR_ACCESO_CLIENTE_NO_ENCONTRADO"


def test_acceso_registra_intento_fallido_en_bitacora(client, datos_acceso, db):
    from app.api.models.acceso import Acceso
    client.post("/api/v1/accesos/entrada",
                json={"documento_identidad": "V-22222222"})
    registro = db.query(Acceso).filter(
        Acceso.cliente_id == datos_acceso["cliente_vencido"].idUsuarios,
        Acceso.acceso_permitido == False,
    ).first()
    assert registro is not None