╔══════════════════════════════════════╗
║   🌸 SmartGym API 🌸                ║
║   Gestión Integral de Gimnasios      ║
╚══════════════════════════════════════╝
> ✨ Plataforma API RESTful para la gestión integral de un gimnasio moderno  
> 🎓 Laboratorio I — 2026-1 · Universidad Centroccidental Lisandro Alvarado

</div>

---

## 🌸 Descripción

**SmartGym** es una API RESTful desarrollada con **FastAPI** y **PostgreSQL** que centraliza la gestión operativa, financiera y administrativa de un gimnasio moderno. Cubre desde el control de acceso físico hasta el seguimiento biométrico de los clientes, con autenticación segura mediante **JWT** y control de acceso basado en roles **RBAC**.

---

## 👩‍💻 Equipo de Desarrollo

<div align="center">

| 👩 Integrante | 🪪 Cédula | 💼 Módulos |
|---|---|---|
| **Michelle Mendoza** | 30.145.993 | Inventario, Máquinas, Tienda POS |
| **Karlianny Márquez** | 28.144.852 | Finanzas, Planes, Clases y Reservas |
| **Mercedes Cordero** | 30.447.476 | Auth, Acceso Físico, Seguridad |

</div>

---

## 🛠️ Stack Tecnológico

<div align="center">

| Tecnología | Uso |
|---|---|
| 🐍 **Python + FastAPI** | Framework principal — alto rendimiento y documentación automática |
| 🐘 **PostgreSQL 15** | Motor relacional con integridad referencial completa |
| 🔐 **JWT + RBAC** | Autenticación por Bearer Token y control por roles |
| ✅ **Pydantic** | Validación estricta de esquemas de entrada y salida |
| 🐳 **Docker + Compose** | Contenerización y despliegue reproducible |
| 📖 **OpenAPI / Swagger** | Documentación interactiva autogenerada en `/api-docs` |

</div>

---

## 🏗️ Arquitectura en Capas

```
💪 SmartGym API
└── 📁 app/
    └── 📁 api/
        ├── 🌐 v1/endpoints/    ← Controladores: rutas y validación de entrada
        ├── 💼 services/         ← Lógica de negocio y reglas del gimnasio
        ├── 🗄️  repositories/   ← Acceso directo a PostgreSQL
        ├── 📐 schemas/          ← Modelos Pydantic de request/response
        ├── 🧩 models/           ← Entidades SQLAlchemy (tablas de la BD)
        ├── ⚙️  core/            ← Config, seguridad y dependencias
        └── 🌱 database/         ← Sesión de BD y Seeders
```

---

## 🔐 Roles del Sistema

| Rol | Permisos |
|---|---|
| 👑 **Administrador** | Control total: usuarios, máquinas, clases, finanzas |
| 💰 **Finanzas** | Pagos, planes de suscripción, ventas y reportes |
| 🏅 **Entrenador** | Ver clases programadas y registrar evaluaciones biométricas |
| 🙋 **Cliente** | Reservar clases, consultar membresía e historial personal |

---

## ⚡ Reglas de Negocio Críticas

| # | Regla | Código de Error |
|---|---|---|
| 1 | 🚫 Un cliente no puede reservar dos clases con horarios solapados | `ERR_RESERVA_SOLAPAMIENTO` |
| 2 | 🚫 No se aceptan reservas si la sesión alcanzó su cupo máximo | `ERR_RESERVA_SIN_CUPOS` |
| 3 | 🚫 El acceso físico se deniega si la membresía está vencida | `ERR_ACCESO_MEMBRESIA_INACTIVA` |
| 4 | 🚫 Los pagos registrados son inmutables (no se pueden editar ni borrar) | `ERR_PAGO_INMUTABLE` |

> Todos los errores retornan **HTTP 409 Conflict** con estructura JSON estricta:
> ```json
> {
>   "error": "Conflict",
>   "codigoInterno": "ERR_RESERVA_SOLAPAMIENTO",
>   "mensaje": "Ya tienes una reserva activa en ese bloque horario.",
>   "timestamp": "2026-06-16T10:00:00Z"
> }
> ```

---

## 🐳 Levantar con Docker (Recomendado)

### Prerequisitos
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) instalados

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476-30.145.993-28.144.852.git
cd lab1-proyecto-2026-1-30447476-30.145.993-28.144.852
```

### 2️⃣ Levantar los servicios
```bash
docker compose up --build
```

Esto levanta automáticamente:
- 🐘 **PostgreSQL** en el puerto `5432`
- 💪 **SmartGym API** en el puerto `8000`

### 3️⃣ Poblar la base de datos
En otra terminal:
```bash
docker exec smartgym_api python -m app.api.database.seeders
```

### 4️⃣ Acceder a la documentación
| Interfaz | URL |
|---|---|
| 📖 Swagger UI | http://localhost:8000/api-docs |
| 📄 ReDoc | http://localhost:8000/redoc |
| 🔧 Health Check | http://localhost:8000/ |

### 5️⃣ Detener los servicios
```bash
docker compose down          # Detiene los contenedores
docker compose down -v       # Detiene y elimina los datos
```

---

## ⚙️ Instalación Local (Sin Docker)

### Prerequisitos
- Python 3.11+
- PostgreSQL corriendo localmente

### Pasos
```bash
# 1. Clonar
git clone https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476-30.145.993-28.144.852.git
cd lab1-proyecto-2026-1-30447476-30.145.993-28.144.852

# 2. Entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\Activate.ps1      # Windows PowerShell

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (.env)
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/smartgym_db
SECRET_KEY=supersecretkey_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 5. Ejecutar seeder
python -m app.api.database.seeders

# 6. Iniciar API
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 🌱 Datos de Prueba (Seeder)

El seeder crea automáticamente todo lo necesario para probar el sistema:

| 📧 Email | 🔑 Contraseña | 👤 Rol |
|---|---|---|
| `admin@smartgym.com` | `Admin2026!` | Administrador |
| `finanzas@smartgym.com` | `Finanzas2026!` | Finanzas |
| `carlos@smartgym.com` | `Entrenador2026!` | Entrenador |
| `laura@smartgym.com` | `Entrenador2026!` | Entrenador |
| `maria@gmail.com` | `Cliente2026!` | Cliente ✅ membresía activa |
| `pedro@gmail.com` | `Cliente2026!` | Cliente ✅ membresía activa |
| `ana@gmail.com` | `Cliente2026!` | Cliente ✅ membresía activa |

También se crean: **4 roles**, **3 categorías de máquinas**, **5 máquinas**, **3 categorías de productos**, **3 productos**, **3 planes de suscripción** y **5 sesiones de clase**.

---

## 📖 Cómo Probar la API

### Desde Swagger UI
1. Abre [http://localhost:8000/api-docs](http://localhost:8000/api-docs)
2. Haz login con `POST /api/v1/auth/login`:
```json
{
  "email": "admin@smartgym.com",
  "password": "Admin2026!"
}
```
3. Copia el `token` de la respuesta
4. Haz clic en **🔓 Authorize** e ingresa: `Bearer <token>`
5. ¡Listo! Ya puedes probar todos los endpoints protegidos

### Secuencia recomendada
```
1. POST /api/v1/auth/login          → Obtener token
2. GET  /api/v1/auth/me             → Verificar perfil
3. GET  /api/v1/maquinas            → Ver inventario
4. GET  /api/v1/sesiones            → Ver clases disponibles
5. POST /api/v1/reservas            → Reservar una clase
6. POST /api/v1/accesos/entrada     → Simular entrada al gimnasio
7. POST /api/v1/tienda/ventas       → Registrar venta
8. POST /api/v1/pagos               → Registrar pago de membresía
```

---

## 📁 Módulos Implementados

| Módulo | Endpoints | Estado |
|---|---|---|
| 🔐 Autenticación y Roles | `/auth`, `/usuarios` | ✅ |
| 🏋️ Inventario de Máquinas | `/maquinas`, `/categorias-maquinas` | ✅ |
| 🔧 Mantenimiento | `/tickets-mantenimiento` | ✅ |
| 🎽 Clases y Disciplinas | `/sesiones`, `/disciplinas`, `/entrenadores` | ✅ |
| 📅 Reservas | `/reservas` | ✅ |
| 🚪 Control de Acceso | `/accesos` | ✅ |
| 💳 Finanzas y Planes | `/planes`, `/pagos`, `/finanzas` | ✅ |
| 📊 Biométrico | `/evaluaciones` | ✅ |
| 🛒 Tienda POS | `/tienda/productos`, `/tienda/ventas` | ✅ |
| 👥 Clientes | `/clientes` | ✅ |

---

<div align="center">

**💪 SmartGym API** · Laboratorio I 2026-1 · UCLA  
Hecho con 🩷 por Michelle Mendoza · Karlianny Márquez · Mercedes Cordero

</div>