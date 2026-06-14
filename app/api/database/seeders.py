from datetime import date, datetime, timedelta
from app.api.database.session import SessionLocal, create_tables
from app.api.core.security import hash_password
from app.api.models.rol import Rol
from app.api.models.usuario import Usuario
from app.api.models.cliente import Cliente
from app.api.models.entrenador import Entrenador
from app.api.models.disciplina import Disciplina
from app.api.models.categoriasMaquinas import CategoriasMaquinas
from app.api.models.maquina import Maquina, EstadoMaquina
from app.api.models.categoriaProducto import CategoriaProducto
from app.api.models.producto import ProductoTienda
from app.api.models.plan import Plan
from app.api.models.sesion import Sesion
from app.api.models.pago import Pago

ROLES = [
    {"nombreRol": "Administrador", "descripcion": "Control total del sistema"},
    {"nombreRol": "Finanzas",      "descripcion": "Gestión de pagos y ventas"},
    {"nombreRol": "Entrenador",    "descripcion": "Gestión de clases y evaluaciones"},
    {"nombreRol": "Cliente",       "descripcion": "Acceso básico al gimnasio"},
]

USUARIOS = [
    {"nombreUsuario": "admin",            "email": "admin@smartgym.com",    "password": "Admin2026!",       "rol": "Administrador", "cedula": "V-00000001"},
    {"nombreUsuario": "finanzas01",       "email": "finanzas@smartgym.com", "password": "Finanzas2026!",    "rol": "Finanzas",      "cedula": "V-00000002"},
    {"nombreUsuario": "carlos_entrenador","email": "carlos@smartgym.com",   "password": "Entrenador2026!",  "rol": "Entrenador",    "cedula": "V-10000001"},
    {"nombreUsuario": "laura_entrenadora","email": "laura@smartgym.com",    "password": "Entrenador2026!",  "rol": "Entrenador",    "cedula": "V-10000002"},
    {"nombreUsuario": "maria_cliente",    "email": "maria@gmail.com",       "password": "Cliente2026!",     "rol": "Cliente",       "cedula": "V-30145993"},
    {"nombreUsuario": "pedro_cliente",    "email": "pedro@gmail.com",       "password": "Cliente2026!",     "rol": "Cliente",       "cedula": "V-28144852"},
    {"nombreUsuario": "ana_cliente",      "email": "ana@gmail.com",         "password": "Cliente2026!",     "rol": "Cliente",       "cedula": "V-30447476"},
]

CATEGORIAS_MAQUINAS = [
    {"nombre": "Cardio",           "descripcion": "Equipos cardiovasculares"},
    {"nombre": "Fuerza libre",     "descripcion": "Mancuernas, barras y discos"},
    {"nombre": "Máquinas guiadas", "descripcion": "Equipos con trayectoria fija"},
]

MAQUINAS = [
    {"nombreMaquina": "Cinta de correr TechRun Pro", "descripcionTecnica": "Velocidad máx 20 km/h, inclinación 0-15%", "estadoOperativo": EstadoMaquina.ACTIVA,           "categoria": "Cardio",           "fechaAdquisicion": date(2024, 3, 10), "numeroSerie": "TR-2024-001"},
    {"nombreMaquina": "Bicicleta estática SpinMax",  "descripcionTecnica": "20 niveles de resistencia",                "estadoOperativo": EstadoMaquina.ACTIVA,           "categoria": "Cardio",           "fechaAdquisicion": date(2024, 3, 10), "numeroSerie": "SM-2024-001"},
    {"nombreMaquina": "Elíptica PowerGlide 3000",    "descripcionTecnica": "Zancada ajustable 18-22 pulgadas",         "estadoOperativo": EstadoMaquina.EN_MANTENIMIENTO, "categoria": "Cardio",           "fechaAdquisicion": date(2023, 8, 15), "numeroSerie": "PG-2023-001"},
    {"nombreMaquina": "Rack de sentadillas olímpico","descripcionTecnica": "Capacidad 500 kg, ajustable",              "estadoOperativo": EstadoMaquina.ACTIVA,           "categoria": "Fuerza libre",     "fechaAdquisicion": date(2023, 6,  1), "numeroSerie": "RS-2023-001"},
    {"nombreMaquina": "Prensa de piernas 45°",       "descripcionTecnica": "Capacidad 400 kg, plataforma antidesl.",   "estadoOperativo": EstadoMaquina.ACTIVA,           "categoria": "Máquinas guiadas", "fechaAdquisicion": date(2024, 2,  5), "numeroSerie": "PP-2024-001"},
]

CATEGORIAS_PRODUCTOS = [
    {"nombre": "Suplementos", "descripcion": "Proteínas, creatinas y vitaminas"},
    {"nombre": "Bebidas",     "descripcion": "Hidratación y bebidas energéticas"},
    {"nombre": "Accesorios",  "descripcion": "Guantes, correas y toallas"},
]

PRODUCTOS = [
    {"nombre": "Proteína Whey Gold 2kg",      "descripcion": "25g proteína por servicio", "categoria": "Suplementos", "precio": 45.99, "stock": 30,  "codigoBarra": "SUP-WH-001"},
    {"nombre": "Agua mineral 500ml",          "descripcion": "Agua natural sin gas",       "categoria": "Bebidas",     "precio":  1.00, "stock": 200, "codigoBarra": "BEB-AG-001"},
    {"nombre": "Toalla microfibra SmartGym",  "descripcion": "Secado rápido, 40x80cm",     "categoria": "Accesorios",  "precio":  8.00, "stock": 60,  "codigoBarra": "ACC-TO-001"},
]

PLANES = [
    {"nombre": "Plan Básico",   "precio":  25.00, "duracion_dias":  30},
    {"nombre": "Plan Estándar", "precio":  65.00, "duracion_dias":  90},
    {"nombre": "Plan Premium",  "precio": 110.00, "duracion_dias": 180},
]

DISCIPLINAS = [
    {"nombre": "Spinning",   "descripcion": "Ciclismo indoor de alta intensidad", "duracionMinutos": 60},
    {"nombre": "Yoga",       "descripcion": "Flexibilidad y meditación",           "duracionMinutos": 60},
    {"nombre": "Crossfit",   "descripcion": "Entrenamiento funcional intensivo",   "duracionMinutos": 60},
    {"nombre": "Zumba",      "descripcion": "Baile aeróbico",                      "duracionMinutos": 60},
    {"nombre": "Funcional",  "descripcion": "Entrenamiento funcional general",     "duracionMinutos": 60},
]


def seed_roles(db):
    print("\n📋 Roles:")
    roles = {}
    for r in ROLES:
        obj = db.query(Rol).filter(Rol.nombreRol == r["nombreRol"]).first()
        if not obj:
            obj = Rol(nombreRol=r["nombreRol"], descripcion=r["descripcion"])
            db.add(obj); db.flush()
            print(f"  ✅ {r['nombreRol']}")
        else:
            print(f"  ⏭  {r['nombreRol']} (ya existe)")
        roles[r["nombreRol"]] = obj
    return roles


def seed_usuarios(db, roles):
    print("\n👤 Usuarios:")
    usuarios = {}
    for u in USUARIOS:
        obj = db.query(Usuario).filter(Usuario.email == u["email"]).first()
        if not obj:
            obj = Usuario(
                nombreUsuario=u["nombreUsuario"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                cedula=u["cedula"],
                rol_id=roles[u["rol"]].idRol,
                activo=True,
            )
            db.add(obj); db.flush()
            print(f"  ✅ {u['email']} [{u['rol']}]")
        else:
            print(f"  ⏭  {u['email']} (ya existe)")
        usuarios[u["email"]] = obj
    return usuarios


def seed_clientes(db, usuarios):
    print("\n🧑 Clientes:")
    clientes_data = [
        {"email": "maria@gmail.com", "nombre": "María",  "apellido": "González", "cedula": "30145993"},
        {"email": "pedro@gmail.com", "nombre": "Pedro",  "apellido": "Ramírez",  "cedula": "28144852"},
        {"email": "ana@gmail.com",   "nombre": "Ana",    "apellido": "Martínez", "cedula": "30447476"},
    ]
    clientes = {}
    for c in clientes_data:
        obj = db.query(Cliente).filter(Cliente.cedula == c["cedula"]).first()
        if not obj:
            usuario = usuarios.get(c["email"])
            obj = Cliente(
                usuario_id=usuario.idUsuarios if usuario else None,
                nombre=c["nombre"],
                apellido=c["apellido"],
                cedula=c["cedula"],
                activo=True,
            )
            db.add(obj); db.flush()
            print(f"  ✅ {c['nombre']} {c['apellido']} (cédula: {c['cedula']})")
        else:
            print(f"  ⏭  {c['nombre']} (ya existe)")
        clientes[c["email"]] = obj
    return clientes


def seed_entrenadores(db, usuarios):
    print("\n🏅 Entrenadores:")
    entrenadores_data = [
        {"email": "carlos@smartgym.com", "nombre": "Carlos", "apellido": "Pérez",  "cedula": "10000001", "especialidad": "Crossfit y Funcional"},
        {"email": "laura@smartgym.com",  "nombre": "Laura",  "apellido": "Torres", "cedula": "10000002", "especialidad": "Yoga y Pilates"},
    ]
    entrenadores = {}
    for e in entrenadores_data:
        obj = db.query(Entrenador).filter(Entrenador.cedula == e["cedula"]).first()
        if not obj:
            usuario = usuarios.get(e["email"])
            obj = Entrenador(
                usuario_id=usuario.idUsuarios if usuario else None,
                nombre=e["nombre"],
                apellido=e["apellido"],
                cedula=e["cedula"],
                especialidad=e["especialidad"],
                activo=True,
            )
            db.add(obj); db.flush()
            print(f"  ✅ {e['nombre']} {e['apellido']}")
        else:
            print(f"  ⏭  {e['nombre']} (ya existe)")
        entrenadores[e["email"]] = obj
    return entrenadores


def seed_disciplinas(db):
    print("\n🎽 Disciplinas:")
    disciplinas = {}
    for d in DISCIPLINAS:
        obj = db.query(Disciplina).filter(Disciplina.nombre == d["nombre"]).first()
        if not obj:
            obj = Disciplina(nombre=d["nombre"], descripcion=d["descripcion"], duracionMinutos=d["duracionMinutos"])
            db.add(obj); db.flush()
            print(f"  ✅ {d['nombre']}")
        else:
            print(f"  ⏭  {d['nombre']} (ya existe)")
        disciplinas[d["nombre"]] = obj
    return disciplinas


def seed_categorias_maquinas(db):
    print("\n🏷  Categorías de máquinas:")
    cats = {}
    for c in CATEGORIAS_MAQUINAS:
        obj = db.query(CategoriasMaquinas).filter(CategoriasMaquinas.nombre == c["nombre"]).first()
        if not obj:
            obj = CategoriasMaquinas(nombre=c["nombre"], descripcion=c["descripcion"])
            db.add(obj); db.flush()
            print(f"  ✅ {c['nombre']}")
        else:
            print(f"  ⏭  {c['nombre']} (ya existe)")
        cats[c["nombre"]] = obj
    return cats


def seed_maquinas(db, cats):
    print("\n🏋️  Máquinas:")
    for m in MAQUINAS:
        obj = db.query(Maquina).filter(Maquina.numeroSerie == m["numeroSerie"]).first()
        if not obj:
            obj = Maquina(
                nombreMaquina=m["nombreMaquina"],
                descripcionTecnica=m["descripcionTecnica"],
                estadoOperativo=m["estadoOperativo"],
                categoria_id=cats[m["categoria"]].idCategoriasMaquinas,
                fechaAdquisicion=m["fechaAdquisicion"],
                numeroSerie=m["numeroSerie"],
            )
            db.add(obj)
            print(f"  ✅ {m['nombreMaquina']}")
        else:
            print(f"  ⏭  {m['nombreMaquina']} (ya existe)")


def seed_categorias_productos(db):
    print("\n🏷  Categorías de productos:")
    cats = {}
    for c in CATEGORIAS_PRODUCTOS:
        obj = db.query(CategoriaProducto).filter(CategoriaProducto.nombre == c["nombre"]).first()
        if not obj:
            obj = CategoriaProducto(nombre=c["nombre"], descripcion=c["descripcion"])
            db.add(obj); db.flush()
            print(f"  ✅ {c['nombre']}")
        else:
            print(f"  ⏭  {c['nombre']} (ya existe)")
        cats[c["nombre"]] = obj
    return cats


def seed_productos(db, cats):
    print("\n🛒 Productos:")
    for p in PRODUCTOS:
        obj = db.query(ProductoTienda).filter(ProductoTienda.codigoBarra == p["codigoBarra"]).first()
        if not obj:
            obj = ProductoTienda(
                nombre=p["nombre"],
                descripcion=p["descripcion"],
                categoriaProducto_id=cats[p["categoria"]].idCategoriaProducto,
                precio=p["precio"],
                stock=p["stock"],
                codigoBarra=p["codigoBarra"],
                activo=True,
            )
            db.add(obj)
            print(f"  ✅ {p['nombre']} [stock: {p['stock']}]")
        else:
            print(f"  ⏭  {p['nombre']} (ya existe)")


def seed_planes(db):
    print("\n💳 Planes:")
    planes = {}
    for p in PLANES:
        obj = db.query(Plan).filter(Plan.nombre == p["nombre"]).first()
        if not obj:
            obj = Plan(nombre=p["nombre"], precio=p["precio"], duracion_dias=p["duracion_dias"])
            db.add(obj); db.flush()
            print(f"  ✅ {p['nombre']} [${p['precio']} / {p['duracion_dias']} días]")
        else:
            print(f"  ⏭  {p['nombre']} (ya existe)")
        planes[p["nombre"]] = obj
    return planes


def seed_sesiones(db, entrenadores, disciplinas):
    print("\n🗓  Sesiones:")
    HOY = date.today()
    sesiones_data = [
        {"disciplina": "Spinning",  "entrenador": "carlos@smartgym.com", "inicio": datetime.combine(HOY + timedelta(days=1), datetime.min.time()).replace(hour=7),  "fin": datetime.combine(HOY + timedelta(days=1), datetime.min.time()).replace(hour=8),  "cupos": 15},
        {"disciplina": "Yoga",      "entrenador": "laura@smartgym.com",  "inicio": datetime.combine(HOY + timedelta(days=1), datetime.min.time()).replace(hour=9),  "fin": datetime.combine(HOY + timedelta(days=1), datetime.min.time()).replace(hour=10), "cupos": 12},
        {"disciplina": "Crossfit",  "entrenador": "carlos@smartgym.com", "inicio": datetime.combine(HOY + timedelta(days=2), datetime.min.time()).replace(hour=6),  "fin": datetime.combine(HOY + timedelta(days=2), datetime.min.time()).replace(hour=7),  "cupos": 10},
        {"disciplina": "Zumba",     "entrenador": "laura@smartgym.com",  "inicio": datetime.combine(HOY + timedelta(days=2), datetime.min.time()).replace(hour=19), "fin": datetime.combine(HOY + timedelta(days=2), datetime.min.time()).replace(hour=20), "cupos": 20},
        {"disciplina": "Funcional", "entrenador": "carlos@smartgym.com", "inicio": datetime.combine(HOY + timedelta(days=3), datetime.min.time()).replace(hour=17), "fin": datetime.combine(HOY + timedelta(days=3), datetime.min.time()).replace(hour=18), "cupos": 12},
    ]
    for s in sesiones_data:
        entrenador = entrenadores.get(s["entrenador"])
        disciplina = disciplinas.get(s["disciplina"])
        if not entrenador or not disciplina:
            print(f"  ⚠️  Faltan datos para sesión {s['disciplina']}, se omite")
            continue
        obj = db.query(Sesion).filter(
            Sesion.disciplina_id == disciplina.idDisciplina,
            Sesion.fecha_hora_inicio == s["inicio"],
        ).first()
        if not obj:
            obj = Sesion(
                disciplina_id=disciplina.idDisciplina,
                entrenador_id=entrenador.idEntrenador,
                fecha_hora_inicio=s["inicio"],
                fecha_hora_fin=s["fin"],
                cupo_maximo=s["cupos"],
                cupos_disponibles=s["cupos"],
                estado="Programada",
            )
            db.add(obj)
            print(f"  ✅ {s['disciplina']} [{s['inicio'].strftime('%H:%M')}-{s['fin'].strftime('%H:%M')} | cupos: {s['cupos']}]")
        else:
            print(f"  ⏭  {s['disciplina']} ese día (ya existe)")


def seed_pagos_demo(db, clientes, planes):
    print("\n💰 Pagos de membresía (demo):")
    pagos_data = [
        ("maria@gmail.com", "Plan Estándar",  65.00),
        ("pedro@gmail.com", "Plan Básico",    25.00),
        ("ana@gmail.com",   "Plan Premium",  110.00),
    ]
    for email, nombre_plan, monto in pagos_data:
        cliente = clientes.get(email)
        plan = planes.get(nombre_plan)
        if not cliente or not plan:
            print(f"  ⚠️  {email} o plan '{nombre_plan}' no encontrado")
            continue
        obj = db.query(Pago).filter(
            Pago.cliente_id == cliente.idCliente,
            Pago.plan_id == plan.id,
        ).first()
        if not obj:
            fecha_pago = datetime.now()
            obj = Pago(
                cliente_id=cliente.idCliente,
                plan_id=plan.id,
                monto=monto,
                fecha_pago=fecha_pago,
                fecha_vencimiento=fecha_pago + timedelta(days=plan.duracion_dias),
                nombre_plan_snapshot=plan.nombre,
                precio_plan_snapshot=plan.precio,
            )
            db.add(obj)
            print(f"  ✅ {email} → {nombre_plan} [${monto:.2f}]")
        else:
            print(f"  ⏭  Pago de {email} (ya existe)")


def seed():
    print("=" * 55)
    print("🌱  SmartGym — Seed de base de datos")
    print("=" * 55)
    print("\n🔨 Creando tablas...")
    create_tables()
    print("✅ Tablas listas")

    db = SessionLocal()
    try:
        roles       = seed_roles(db)
        usuarios    = seed_usuarios(db, roles)
        clientes    = seed_clientes(db, usuarios)
        entrenadores = seed_entrenadores(db, usuarios)
        disciplinas = seed_disciplinas(db)
        cats_maq    = seed_categorias_maquinas(db)
        seed_maquinas(db, cats_maq)
        cats_prod   = seed_categorias_productos(db)
        seed_productos(db, cats_prod)
        planes      = seed_planes(db)
        seed_sesiones(db, entrenadores, disciplinas)
        seed_pagos_demo(db, clientes, planes)
        db.commit()
        print("\n" + "=" * 55)
        print("✅  Seed completado exitosamente")
        print("=" * 55)
        print("\n📌 Credenciales:")
        print("  admin@smartgym.com     → Admin2026!      [Administrador]")
        print("  finanzas@smartgym.com  → Finanzas2026!   [Finanzas]")
        print("  carlos@smartgym.com    → Entrenador2026! [Entrenador]")
        print("  laura@smartgym.com     → Entrenador2026! [Entrenador]")
        print("  maria@gmail.com        → Cliente2026!    [Cliente]")
        print("  pedro@gmail.com        → Cliente2026!    [Cliente]")
        print("  ana@gmail.com          → Cliente2026!    [Cliente]")
        print("\n📚 Documentación: http://localhost:8000/api-docs")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante el seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()