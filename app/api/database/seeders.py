from datetime import date, datetime, time, timedelta
from app.api.database.session import SessionLocal, create_tables
from app.api.core.security import hash_password
from app.api.models.rol import Rol
from app.api.models.usuario import Usuario
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
    {
        "nombreUsuario": "admin",
        "email":         "admin@smartgym.com",
        "password":      "Admin2026!",
        "rol":           "Administrador",
        "cedula":        "V-00000001",
    },
    {
        "nombreUsuario": "finanzas01",
        "email":         "finanzas@smartgym.com",
        "password":      "Finanzas2026!",
        "rol":           "Finanzas",
        "cedula":        "V-00000002",
    },
    {
        "nombreUsuario": "carlos_entrenador",
        "email":         "carlos@smartgym.com",
        "password":      "Entrenador2026!",
        "rol":           "Entrenador",
        "cedula":        "V-10000001",
    },
    {
        "nombreUsuario": "laura_entrenadora",
        "email":         "laura@smartgym.com",
        "password":      "Entrenador2026!",
        "rol":           "Entrenador",
        "cedula":        "V-10000002",
    },
    {
        "nombreUsuario": "maria_cliente",
        "email":         "maria@gmail.com",
        "password":      "Cliente2026!",
        "rol":           "Cliente",
        "cedula":        "V-30145993",
    },
    {
        "nombreUsuario": "pedro_cliente",
        "email":         "pedro@gmail.com",
        "password":      "Cliente2026!",
        "rol":           "Cliente",
        "cedula":        "V-28144852",
    },
    {
        "nombreUsuario": "ana_cliente",
        "email":         "ana@gmail.com",
        "password":      "Cliente2026!",
        "rol":           "Cliente",
        "cedula":        "V-30447476",
    },
]

CATEGORIAS_MAQUINAS = [
    {"nombre": "Cardio",           "descripcion": "Equipos para ejercicio cardiovascular"},
    {"nombre": "Fuerza libre",     "descripcion": "Mancuernas, barras y discos"},
    {"nombre": "Máquinas guiadas", "descripcion": "Equipos con trayectoria fija de movimiento"},
    {"nombre": "Funcional",        "descripcion": "Equipos para entrenamiento funcional y crossfit"},
    {"nombre": "Estiramiento",     "descripcion": "Equipos de movilidad y recuperación"},
]


MAQUINAS = [
    # Cardio
    {
        "nombreMaquina":      "Cinta de correr TechRun Pro",
        "descripcionTecnica": "Velocidad máx 20 km/h, inclinación 0–15%, pantalla táctil",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Cardio",
        "fechaAdquisicion":   date(2024, 3, 10),
        "numeroSerie":        "TR-2024-001",
    },
    {
        "nombreMaquina":      "Bicicleta estática SpinMax",
        "descripcionTecnica": "20 niveles de resistencia, monitor de frecuencia cardiaca",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Cardio",
        "fechaAdquisicion":   date(2024, 3, 10),
        "numeroSerie":        "SM-2024-001",
    },
    {
        "nombreMaquina":      "Elíptica PowerGlide 3000",
        "descripcionTecnica": "Zancada ajustable 18–22 pulgadas, volante de 20 kg",
        "estadoOperativo":    EstadoMaquina.EN_MANTENIMIENTO,
        "categoria":          "Cardio",
        "fechaAdquisicion":   date(2023, 8, 15),
        "numeroSerie":        "PG-2023-001",
    },
    {
        "nombreMaquina":      "Remo Concept2 Model D",
        "descripcionTecnica": "Monitor PM5, resistencia de aire, plegable",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Cardio",
        "fechaAdquisicion":   date(2024, 1, 20),
        "numeroSerie":        "C2-2024-001",
    },
    # Fuerza libre
    {
        "nombreMaquina":      "Rack de sentadillas olímpico",
        "descripcionTecnica": "Capacidad 500 kg, ajustable, incluye barras J",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Fuerza libre",
        "fechaAdquisicion":   date(2023, 6, 1),
        "numeroSerie":        "RS-2023-001",
    },
    {
        "nombreMaquina":      "Banco ajustable FitPro",
        "descripcionTecnica": "Plano, inclinado y declinado, acolchado anti-deslizante",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Fuerza libre",
        "fechaAdquisicion":   date(2023, 6, 1),
        "numeroSerie":        "BA-2023-001",
    },
    # Máquinas guiadas
    {
        "nombreMaquina":      "Prensa de piernas 45°",
        "descripcionTecnica": "Capacidad 400 kg, plataforma antideslizante, asiento ajustable",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Máquinas guiadas",
        "fechaAdquisicion":   date(2024, 2, 5),
        "numeroSerie":        "PP-2024-001",
    },
    {
        "nombreMaquina":      "Jalón al pecho TechGym",
        "descripcionTecnica": "Stack 100 kg, doble polea, barra larga y cuerda incluidas",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Máquinas guiadas",
        "fechaAdquisicion":   date(2024, 2, 5),
        "numeroSerie":        "JP-2024-001",
    },
    {
        "nombreMaquina":      "Extensión de cuádriceps",
        "descripcionTecnica": "Stack 80 kg, biomecánica de eje rotacional",
        "estadoOperativo":    EstadoMaquina.FUERA_DE_SERVICIO,
        "categoria":          "Máquinas guiadas",
        "fechaAdquisicion":   date(2022, 11, 3),
        "numeroSerie":        "EC-2022-001",
    },
    # Funcional
    {
        "nombreMaquina":      "Cajones pliométricos (set 3)",
        "descripcionTecnica": "Alturas 30 / 45 / 60 cm, madera con revestimiento antideslizante",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Funcional",
        "fechaAdquisicion":   date(2024, 4, 12),
        "numeroSerie":        "CP-2024-001",
    },
    {
        "nombreMaquina":      "TRX Suspension Trainer PRO",
        "descripcionTecnica": "Ancla de techo, correas ajustables, capacidad 160 kg",
        "estadoOperativo":    EstadoMaquina.ACTIVA,
        "categoria":          "Funcional",
        "fechaAdquisicion":   date(2024, 4, 12),
        "numeroSerie":        "TRX-2024-001",
    },
]

CATEGORIAS_PRODUCTOS = [
    {"nombre": "Suplementos",    "descripcion": "Proteínas, creatinas, aminoácidos y vitaminas"},
    {"nombre": "Bebidas",        "descripcion": "Hidratación y bebidas energéticas"},
    {"nombre": "Accesorios",     "descripcion": "Guantes, correas, cinturones y toallas"},
    {"nombre": "Indumentaria",   "descripcion": "Ropa deportiva y calzado"},
    {"nombre": "Snacks fitness", "descripcion": "Barras proteicas y alimentos saludables"},
]

# ── Productos de tienda ────────────────────────────────────────────────────
PRODUCTOS = [
    # Suplementos
    {
        "nombre":             "Proteína Whey Gold 2kg",
        "descripcion":        "25g proteína por servicio, sabor chocolate, 67 porciones",
        "categoria":          "Suplementos",
        "precio":             45.99,
        "stock":              30,
        "codigoBarra":       "SUP-WH-001",
    },
    {
        "nombre":             "Creatina Monohidratada 300g",
        "descripcion":        "Micronizada, 5g por porción, sin sabor",
        "categoria":          "Suplementos",
        "precio":             18.50,
        "stock":              25,
        "codigoBarra":       "SUP-CR-001",
    },
    {
        "nombre":             "BCAA 2:1:1 Aminoácidos 400g",
        "descripcion":        "Leucina, Isoleucina, Valina. Sabor sandía",
        "categoria":          "Suplementos",
        "precio":             22.00,
        "stock":              20,
        "codigoBarra":       "SUP-BC-001",
    },
    {
        "nombre":             "Multivitamínico Sport 60 tabs",
        "descripcion":        "Fórmula completa para deportistas, 2 meses de suministro",
        "categoria":          "Suplementos",
        "precio":             12.75,
        "stock":              40,
        "codigoBarra":       "SUP-MV-001",
    },
    # Bebidas
    {
        "nombre":             "Agua mineral 500ml",
        "descripcion":        "Agua natural sin gas, fría",
        "categoria":          "Bebidas",
        "precio":             1.00,
        "stock":              200,
        "codigoBarra":       "BEB-AG-001",
    },
    {
        "nombre":             "Bebida isotónica Gatorade 600ml",
        "descripcion":        "Repone electrolitos, sabores variados",
        "categoria":          "Bebidas",
        "precio":             2.50,
        "stock":              80,
        "codigoBarra":       "BEB-GT-001",
    },
    {
        "nombre":             "Pre-workout energizante 250ml",
        "descripcion":        "Cafeína + taurina + vitamina B12, sabor naranja",
        "categoria":          "Bebidas",
        "precio":             3.75,
        "stock":              50,
        "codigoBarra":       "BEB-PW-001",
    },
    # Accesorios
    {
        "nombre":             "Guantes de entrenamiento M",
        "descripcion":        "Cuero sintético, palma acolchada, talla M",
        "categoria":          "Accesorios",
        "precio":             14.99,
        "stock":              15,
        "codigoBarra":       "ACC-GU-001",
    },
    {
        "nombre":             "Cinturón lumbar de pesas",
        "descripcion":        "Cuero genuino 10cm, tallas S–XL",
        "categoria":          "Accesorios",
        "precio":             28.00,
        "stock":              10,
        "codigoBarra":       "ACC-CI-001",
    },
    {
        "nombre":             "Toalla microfibra SmartGym",
        "descripcion":        "Secado rápido, 40x80cm, logo bordado",
        "categoria":          "Accesorios",
        "precio":             8.00,
        "stock":              60,
        "codigoBarra":       "ACC-TO-001",
    },
    # Snacks fitness
    {
        "nombre":             "Barra proteica Quest 60g",
        "descripcion":        "21g proteína, 4g azúcar, sabores variados",
        "categoria":          "Snacks fitness",
        "precio":             3.25,
        "stock":              100,
        "codigoBarra":       "SNK-QU-001",
    },
    {
        "nombre":             "Mix de frutos secos 150g",
        "descripcion":        "Almendras, nueces, maní y arándanos sin azúcar añadida",
        "categoria":          "Snacks fitness",
        "precio":             4.50,
        "stock":              45,
        "codigoBarra":       "SNK-FS-001",
    },
]

PLANES = [
    {
        "nombre":        "Plan Básico",
        "precio":        25.00,
        "duracion_dias": 30,
    },
    {
        "nombre":        "Plan Estándar",
        "precio":        65.00,
        "duracion_dias": 90,
    },
    {
        "nombre":        "Plan Premium",
        "precio":        110.00,
        "duracion_dias": 180,
    },
    {
        "nombre":        "Plan Anual",
        "precio":        180.00,
        "duracion_dias": 365,
    },
]

# Se crean con referencia al entrenador después de crear usuarios
HOY = date.today()

SESIONES = [
    {
        "disciplina":   "Spinning",
        "entrenador":   "carlos@smartgym.com",
        "fecha":        datetime.combine(HOY + timedelta(days=1), datetime.min.time()).replace(hour=7),
        "hora_inicio":  "07:00",
        "hora_fin":     "08:00",
        "cupo_maximo":  15,
    },
    {
        "disciplina":   "Yoga",
        "entrenador":   "laura@smartgym.com",
        "fecha":        datetime.combine(HOY + timedelta(days=1), datetime.min.time()).replace(hour=9),
        "hora_inicio":  "09:00",
        "hora_fin":     "10:00",
        "cupo_maximo":  12,
    },
    {
        "disciplina":   "Crossfit",
        "entrenador":   "carlos@smartgym.com",
        "fecha":        datetime.combine(HOY + timedelta(days=2), datetime.min.time()).replace(hour=6),
        "hora_inicio":  "06:00",
        "hora_fin":     "07:00",
        "cupo_maximo":  10,
    },
    {
        "disciplina":   "Pilates",
        "entrenador":   "laura@smartgym.com",
        "fecha":        datetime.combine(HOY + timedelta(days=2), datetime.min.time()).replace(hour=10),
        "hora_inicio":  "10:00",
        "hora_fin":     "11:00",
        "cupo_maximo":  8,
    },
    {
        "disciplina":   "Funcional",
        "entrenador":   "carlos@smartgym.com",
        "fecha":        datetime.combine(HOY + timedelta(days=3), datetime.min.time()).replace(hour=17),
        "hora_inicio":  "17:00",
        "hora_fin":     "18:00",
        "cupo_maximo":  12,
    },
    {
        "disciplina":   "Zumba",
        "entrenador":   "laura@smartgym.com",
        "fecha":        datetime.combine(HOY + timedelta(days=3), datetime.min.time()).replace(hour=19),
        "hora_inicio":  "19:00",
        "hora_fin":     "20:00",
        "cupo_maximo":  20,
    },
]


# ═══════════════════════════════════════════════════════════════════════════
#  FUNCIONES DE SEED POR MÓDULO
# ═══════════════════════════════════════════════════════════════════════════

def seed_roles(db) -> dict:
    """Crea los roles del sistema. Retorna dict {nombreRol: Rol}."""
    print("\n📋 Roles:")
    roles = {}
    for r in ROLES:
        existente = db.query(Rol).filter(Rol.nombreRol == r["nombreRol"]).first()
        if not existente:
            rol = Rol(nombreRol=r["nombreRol"], descripcion=r["descripcion"])
            db.add(rol)
            db.flush()
            roles[r["nombreRol"]] = rol
            print(f"  ✅ {r['nombreRol']}")
        else:
            roles[r["nombreRol"]] = existente
            print(f"  ⏭  {r['nombreRol']} (ya existe)")
    return roles


def seed_usuarios(db, roles: dict) -> dict:
    """Crea los usuarios iniciales. Retorna dict {email: Usuario}."""
    print("\n👤 Usuarios:")
    usuarios = {}
    for u in USUARIOS:
        existente = db.query(Usuario).filter(Usuario.email == u["email"]).first()
        if not existente:
            nuevo = Usuario(
                nombreUsuario=u["nombreUsuario"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                rol_id=roles[u["rol"]].idRol,
                activo=True,
            )
            db.add(nuevo)
            db.flush()
            usuarios[u["email"]] = nuevo
            print(f"  ✅ {u['email']}  [{u['rol']}]  pass: {u['password']}")
        else:
            usuarios[u["email"]] = existente
            print(f"  ⏭  {u['email']} (ya existe)")
    return usuarios


def seed_categorias_maquinas(db) -> dict:
    """Crea categorías de máquinas. Retorna dict {nombre: CategoriasMaquinas}."""
    print("\n🏷  Categorías de máquinas:")
    cats = {}
    for c in CATEGORIAS_MAQUINAS:
        existente = db.query(CategoriasMaquinas).filter(
            CategoriasMaquinas.nombre == c["nombre"]
        ).first()
        if not existente:
            cat = CategoriasMaquinas(nombre=c["nombre"], descripcion=c["descripcion"])
            db.add(cat)
            db.flush()
            cats[c["nombre"]] = cat
            print(f"  ✅ {c['nombre']}")
        else:
            cats[c["nombre"]] = existente
            print(f"  ⏭  {c['nombre']} (ya existe)")
    return cats


def seed_maquinas(db, cats: dict):
    """Crea las máquinas del gimnasio."""
    print("\n🏋️  Máquinas:")
    for m in MAQUINAS:
        existente = db.query(Maquina).filter(
            Maquina.numeroSerie == m["numeroSerie"]
        ).first()
        if not existente:
            maquina = Maquina(
                nombreMaquina=m["nombreMaquina"],
                descripcionTecnica=m["descripcionTecnica"],
                estadoOperativo=m["estadoOperativo"],
                categoria_id=cats[m["categoria"]].idCategoriasMaquinas,
                fechaAdquisicion=m["fechaAdquisicion"],
                numeroSerie=m["numeroSerie"],
            )
            db.add(maquina)
            estado_str = m["estadoOperativo"].value
            print(f"  ✅ {m['nombreMaquina']}  [{estado_str}]")
        else:
            print(f"  ⏭  {m['nombreMaquina']} (ya existe)")


def seed_categorias_productos(db) -> dict:
    """Crea categorías de productos. Retorna dict {nombre: CategoriaProducto}."""
    print("\n🏷  Categorías de productos:")
    cats = {}
    for c in CATEGORIAS_PRODUCTOS:
        existente = db.query(CategoriaProducto).filter(
            CategoriaProducto.nombre == c["nombre"]
        ).first()
        if not existente:
            cat = CategoriaProducto(nombre=c["nombre"], descripcion=c["descripcion"])
            db.add(cat)
            db.flush()
            cats[c["nombre"]] = cat
            print(f"  ✅ {c['nombre']}")
        else:
            cats[c["nombre"]] = existente
            print(f"  ⏭  {c['nombre']} (ya existe)")
    return cats


def seed_productos(db, cats: dict):
    """Crea el inventario inicial de la tienda."""
    print("\n🛒 Productos de tienda:")
    for p in PRODUCTOS:
        existente = db.query(ProductoTienda).filter(
            ProductoTienda.codigoBarra == p["codigoBarra"]
        ).first()
        if not existente:
            producto = ProductoTienda(
                nombre=p["nombre"],
                descripcion=p["descripcion"],
                categoriaProducto_id=cats[p["categoria"]].idCategoriaProducto,
                precio=p["precio"],
                stock=p["stock"],
                codigoBarra=p["codigoBarra"],
                activo=True,
            )
            db.add(producto)
            print(f"  ✅ {p['nombre']}  [stock: {p['stock']} | ${p['precio']:.2f}]")
        else:
            print(f"  ⏭  {p['nombre']} (ya existe)")


def seed_planes(db) -> dict:
    """Crea los planes de membresía. Retorna dict {nombre: Plan}."""
    print("\n💳 Planes de membresía:")
    planes = {}
    for p in PLANES:
        existente = db.query(Plan).filter(Plan.nombre == p["nombre"]).first()
        if not existente:
            plan = Plan(
                nombre=p["nombre"],
                precio=p["precio"],
                duracion_dias=p["duracion_dias"],
            )
            db.add(plan)
            db.flush()
            planes[p["nombre"]] = plan
            print(f"  ✅ {p['nombre']}  [${p['precio']:.2f} / {p['duracion_dias']} días]")
        else:
            planes[p["nombre"]] = existente
            print(f"  ⏭  {p['nombre']} (ya existe)")
    return planes


def seed_sesiones(db, usuarios: dict):
    """Crea sesiones de entrenamiento de muestra."""
    print("\n🗓  Sesiones de entrenamiento:")
    for s in SESIONES:
        entrenador = usuarios.get(s["entrenador"])
        if not entrenador:
            print(f"  ⚠️  Entrenador {s['entrenador']} no encontrado, se omite sesión")
            continue

        existente = db.query(Sesion).filter(
            Sesion.disciplina == s["disciplina"],
            Sesion.fecha == s["fecha"],
            Sesion.entrenador_id == entrenador.idUsuarios,
        ).first()
        if not existente:
            hora_inicio = datetime.strptime(s["hora_inicio"], "%H:%M").time()
            hora_fin = datetime.strptime(s["hora_fin"], "%H:%M").time()
            sesion = Sesion(
                disciplina=s["disciplina"],
                entrenador_id=entrenador.idUsuarios,
                fecha=s["fecha"],
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                cupo_maximo=s["cupo_maximo"],
                cupos_disponibles=s["cupo_maximo"],
            )
            db.add(sesion)
            print(f"  ✅ {s['disciplina']}  [{s['hora_inicio']}–{s['hora_fin']} | cupos: {s['cupo_maximo']}]")
        else:
            print(f"  ⏭  {s['disciplina']} ese día (ya existe)")


def seed_pagos_demo(db, usuarios: dict, planes: dict):
    """
    Crea pagos de membresía para los clientes de prueba.
    Solo se ejecuta si los clientes y planes ya existen.
    """
    print("\n💰 Pagos de membresía (demo):")
    clientes_pagos = [
        ("maria@gmail.com", "Plan Estándar",  90.00),
        ("pedro@gmail.com", "Plan Básico",    25.00),
        ("ana@gmail.com",   "Plan Premium",  110.00),
    ]
    for email, nombre_plan, monto in clientes_pagos:
        cliente = usuarios.get(email)
        plan = planes.get(nombre_plan)
        if not cliente or not plan:
            print(f"  ⚠️  {email} o plan '{nombre_plan}' no encontrado, se omite")
            continue

        existente = db.query(Pago).filter(
            Pago.cliente_id == cliente.idUsuarios,
            Pago.plan_id == plan.id,
        ).first()
        if not existente:
            fecha_pago = datetime.now()
            fecha_vencimiento = fecha_pago + timedelta(days=plan.duracion_dias)
            pago = Pago(
                cliente_id=cliente.idUsuarios,
                plan_id=plan.id,
                monto=monto,
                fecha_pago=fecha_pago,
                fecha_vencimiento=fecha_vencimiento,
            )
            db.add(pago)
            print(f"  ✅ {email}  →  {nombre_plan}  [${monto:.2f}]")
        else:
            print(f"  ⏭  Pago de {email} (ya existe)")


# ═══════════════════════════════════════════════════════════════════════════
#  FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def seed():
    """Ejecuta todos los seeders en orden respetando dependencias."""
    print("=" * 55)
    print("🌱  SmartGym — Seed de base de datos")
    print("=" * 55)

    # 1. Crear tablas
    print("\n🔨 Creando tablas...")
    create_tables()
    print("✅ Tablas listas")

    db = SessionLocal()
    try:
        # 2. Datos base (dependen entre sí)
        roles    = seed_roles(db)
        usuarios = seed_usuarios(db, roles)

        # 3. Módulo Michelle — máquinas e inventario
        cats_maquinas  = seed_categorias_maquinas(db)
        seed_maquinas(db, cats_maquinas)
        cats_productos = seed_categorias_productos(db)
        seed_productos(db, cats_productos)

        # 4. Módulo Karlianny — membresías y agenda
        planes = seed_planes(db)
        seed_sesiones(db, usuarios)
        seed_pagos_demo(db, usuarios, planes)

        # 5. Confirmar todo en una sola transacción
        db.commit()

        print("\n" + "=" * 55)
        print("✅  Seed completado exitosamente")
        print("=" * 55)
        print("\n📌 Credenciales de acceso:")
        print("  admin@smartgym.com       →  Admin2026!   [Administrador]")
        print("  finanzas@smartgym.com    →  Finanzas2026! [Finanzas]")
        print("  carlos@smartgym.com      →  Entrenador2026! [Entrenador]")
        print("  laura@smartgym.com       →  Entrenador2026! [Entrenador]")
        print("  maria@gmail.com          →  Cliente2026!  [Cliente]")
        print("  pedro@gmail.com          →  Cliente2026!  [Cliente]")
        print("  ana@gmail.com            →  Cliente2026!  [Cliente]")
        print("\n📚 Documentación: http://localhost:8000/docs")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante el seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
