import pytest
from tests.conftest import crear_rol, crear_usuario, token_para


@pytest.fixture()
def datos_auth(db):
    rol_admin  = crear_rol(db, "Administrador")
    rol_client = crear_rol(db, "Cliente")
    from app.api.models.rol import Rol
    admin = crear_usuario(db, "adm_auth", "adm_auth@gym.com", "Admin2026!", rol_id=rol_admin.idRol)
    admin.rol = db.query(Rol).filter_by(idRol=rol_admin.idRol).first()
    return {"admin": admin, "rol_admin_id": rol_admin.idRol, "rol_client_id": rol_client.idRol}


def test_login_exitoso(client, datos_auth):
    resp = client.post("/api/v1/auth/login",
                       json={"email": "adm_auth@gym.com", "password": "Admin2026!"})
    assert resp.status_code == 200
    assert "token" in resp.json()


def test_login_password_incorrecto(client, datos_auth):
    resp = client.post("/api/v1/auth/login",
                       json={"email": "adm_auth@gym.com", "password": "Incorrecto!"})
    assert resp.status_code == 401


def test_login_email_inexistente(client, datos_auth):
    resp = client.post("/api/v1/auth/login",
                       json={"email": "noexiste@gym.com", "password": "Admin2026!"})
    assert resp.status_code == 401


def test_registro_usuario_exitoso(client, datos_auth):
    resp = client.post("/api/v1/auth/register", json={
        "nombreUsuario": "nuevo_usr",
        "email": "nuevo@gym.com",
        "password": "NuevoPass1!",
        "rol_id": datos_auth["rol_client_id"],
        "cedula": "V-55555555",
    })
    assert resp.status_code == 201


def test_registro_email_duplicado(client, datos_auth):
    payload = {"nombreUsuario": "dup_a", "email": "dup@gym.com",
               "password": "Pass1234!", "rol_id": datos_auth["rol_client_id"]}
    client.post("/api/v1/auth/register", json=payload)
    payload["nombreUsuario"] = "dup_b"
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_mi_perfil_con_token(client, datos_auth):
    token = token_para(datos_auth["admin"])
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["data"]["email"] == "adm_auth@gym.com"


def test_mi_perfil_sin_token(client, datos_auth):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code in (401, 403)