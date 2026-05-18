from app.api.database.session import SessionLocal, create_tables
from app.api.models.rol import Rol
from app.api.models.usuario import Usuario
from app.api.core.security import hash_password

ROLES = [
    {"nombreRol": "Administrador", "descripcion": "Control total del sistema"},
    {"nombreRol": "Finanzas",      "descripcion": "Gestión de pagos"},
    {"nombreRol": "Entrenador",    "descripcion": "Gestión de clases"},
    {"nombreRol": "Cliente",       "descripcion": "Acceso básico"},
]

ADMIN = {
    "nombreUsuario": "admin",
    "email":         "admin@smartgym.com",
    "password":      "Admin2026!",
}


def seed():
    print("🌱 Creando tablas...")
    create_tables()
    print("✅ Tablas creadas")

    db = SessionLocal()
    try:
        roles = {}
        for r in ROLES:
            existe = db.query(Rol).filter(
                Rol.nombreRol == r["nombreRol"]
            ).first()
            if not existe:
                rol = Rol(**r)
                db.add(rol)
                db.flush()
                roles[r["nombreRol"]] = rol
                print(f"  ✅ Rol creado: {r['nombreRol']}")
            else:
                roles[r["nombreRol"]] = existe
                print(f"  ⏭  Rol ya existe: {r['nombreRol']}")

        admin = db.query(Usuario).filter(
            Usuario.email == ADMIN["email"]
        ).first()
        if not admin:
            nuevo = Usuario(
                nombreUsuario = ADMIN["nombreUsuario"],
                email         = ADMIN["email"],
                password_hash = hash_password(ADMIN["password"]),
                rol_id        = roles["Administrador"].idRol,
                activo        = True,
            )
            db.add(nuevo)
            print(f"  ✅ Admin: {ADMIN['email']} / {ADMIN['password']}")
        else:
            print(f"  ⏭  Admin ya existe")

        db.commit()
        print("\n✅ Seed completado")
    finally:
        db.close()


if __name__ == "__main__":
    seed()