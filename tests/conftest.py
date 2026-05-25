import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.database.session import Base, get_db
from app.api.core.security import hash_password, create_access_token
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_temp.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    import app.api.models  # noqa
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def crear_rol(db, nombre: str, descripcion: str = ""):
    from app.api.models.rol import Rol
    rol = Rol(nombreRol=nombre, descripcion=descripcion)
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


def crear_usuario(db, nombre, email, password, rol_id, cedula=None, activo=True):
    from app.api.models.usuario import Usuario
    u = Usuario(
        nombreUsuario=nombre,
        email=email,
        password_hash=hash_password(password),
        rol_id=rol_id,
        activo=activo,
        cedula=cedula,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def crear_plan(db, nombre, precio, duracion_dias):
    from app.api.models.plan import Plan
    p = Plan(nombre=nombre, precio=precio, duracion_dias=duracion_dias)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def crear_pago(db, cliente_id, plan_id, monto, dias_offset=30):
    from datetime import datetime, timedelta
    from app.api.models.pago import Pago
    ahora = datetime.now()
    p = Pago(
        cliente_id=cliente_id,
        plan_id=plan_id,
        monto=monto,
        fecha_pago=ahora,
        fecha_vencimiento=ahora + timedelta(days=dias_offset),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def token_para(usuario) -> str:
    return create_access_token({
        "sub":    str(usuario.idUsuarios),
        "email":  usuario.email,
        "rol":    usuario.rol.nombreRol if usuario.rol else "Cliente",
        "activo": True,
    })