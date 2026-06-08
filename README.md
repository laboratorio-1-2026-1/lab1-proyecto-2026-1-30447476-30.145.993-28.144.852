# 🏋️ SmartGym API

> Plataforma API para Gestión Integral de Gimnasios  
> **Laboratorio I — 2026-1**

---

## 📌 Descripción

SmartGym es una API RESTful desarrollada con **FastAPI** y **PostgreSQL** que permite la gestión integral de un gimnasio, incluyendo control de acceso, membresías, reservas, máquinas, finanzas y seguimiento biométrico. Implementa autenticación segura mediante **JWT** y control de acceso basado en roles (**RBAC**).

---

## 👥 Integrantes

| Nombre | Cédula |
|---|---|
| Michelle Mendoza | 30.145.993 |
| Karlianny Márquez | 28.144.852 |
| Mercedes Cordero | 30.447.476 |

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| **Python + FastAPI** | Framework principal para la API |
| **PostgreSQL** | Motor de base de datos relacional |
| **JWT + RBAC** | Autenticación y control de acceso por roles |
| **Pydantic** | Validación y esquemas de datos |
| **Docker** | Despliegue y portabilidad |
| **OpenAPI / Swagger** | Documentación automática interactiva |

---

## 🏗️ Arquitectura

El proyecto está organizado en **tres capas principales**:

```
📁 app/
└── 📁 api/
    ├── 🌐 v1/endpoints/   # Controladores — Rutas y validación de entrada
    ├── 💼 services/        # Servicios — Lógica de negocio
    ├── 🗄️ repositories/   # Repositorios — Comunicación con PostgreSQL
    ├── 📐 schemas/         # Esquemas Pydantic — Validación de datos
    ├── 🧩 models/          # Modelos SQLAlchemy — Entidades de la BD
    ├── ⚙️ core/            # Configuración, seguridad y dependencias
    └── 🌱 database/        # Seeders y sesión de base de datos
```

---

## 🔐 Roles del Sistema

El sistema implementa **4 roles** con permisos diferenciados:

| Rol | Permisos |
|---|---|
| **Administración** | Acceso total al sistema |
| **Finanzas** | Gestión de pagos e inventario financiero |
| **Entrenadores** | Gestión de rutinas y clientes asignados |
| **Clientes** | Reservas, membresías y seguimiento personal |

---

## 🐳 Levantar con Docker (Recomendado)

Este es el método oficial de despliegue. Levanta la API y PostgreSQL con un solo comando.

### Prerequisitos
- Tener instalado [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)

### 1. Clonar el repositorio
```bash
git clone https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852.git
cd lab1-proyecto-2026-1-30447476--30.145.993-28.144.852
```

### 2. Levantar los servicios
```bash
docker compose up --build
```

Esto levanta automáticamente:
- **PostgreSQL** en el puerto `5432`
- **SmartGym API** en el puerto `8000`

### 3. Poblar la base de datos con datos de prueba
En otra terminal, ejecuta el seeder:
```bash
docker exec smartgym_api python -m app.api.database.seeders
```

### 4. Acceder a la API
- **Swagger UI:** [http://localhost:8000/api-docs](http://localhost:8000/api-docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 5. Detener los servicios
```bash
docker compose down
```

Para eliminar también los datos de la base de datos:
```bash
docker compose down -v
```

---

## ⚙️ Instalación Local (Sin Docker)

### Prerequisitos
- Python 3.11+
- PostgreSQL instalado y corriendo localmente

### 1. Clonar el repositorio
```bash
git clone https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852.git
cd lab1-proyecto-2026-1-30447476--30.145.993-28.144.852
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos PostgreSQL
Crea una base de datos en tu PostgreSQL local y define la variable de entorno `DATABASE_URL`:

```bash
# Linux/Mac
export DATABASE_URL='postgresql://usuario:contraseña@localhost:5432/smartgym_db'

# Windows PowerShell
$env:DATABASE_URL = 'postgresql://usuario:contraseña@localhost:5432/smartgym_db'
```

O crea un archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/smartgym_db
SECRET_KEY=supersecretkey_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Poblar la base de datos con datos de prueba
```bash
python -m app.api.database.seeders
```

### 6. Ejecutar la API
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 🌱 Datos de Prueba (Seeder)

Al ejecutar el seeder se crean automáticamente los siguientes usuarios:

| Email | Contraseña | Rol |
|---|---|---|
| `admin@smartgym.com` | `Admin2026!` | Administración |
| `finanzas@smartgym.com` | `Finanzas2026!` | Finanzas |
| `carlos@smartgym.com` | `Entrenador2026!` | Entrenador |
| `laura@smartgym.com` | `Entrenador2026!` | Entrenador |
| `maria@gmail.com` | `Cliente2026!` | Cliente |
| `pedro@gmail.com` | `Cliente2026!` | Cliente |
| `ana@gmail.com` | `Cliente2026!` | Cliente |

También se crean: roles, categorías de máquinas, máquinas, planes de suscripción y productos de tienda.

---

## 📖 Documentación y Pruebas

### Probar desde Swagger
1. Abre [http://localhost:8000/api-docs](http://localhost:8000/api-docs)
2. Usa `POST /api/v1/auth/login` con las credenciales de prueba:
```json
{
  "email": "admin@smartgym.com",
  "password": "Admin2026!"
}
```
3. Copia el `token` de la respuesta.
4. Haz clic en **Authorize** e ingresa: `Bearer <token>`
5. Ya puedes probar cualquier endpoint protegido.

### Secuencia recomendada de pruebas
1. Login con `POST /api/v1/auth/login`
2. Verificar usuario con `GET /api/v1/auth/me`
3. Consultar recursos: `/api/v1/maquinas`, `/api/v1/sesiones`, `/api/v1/planes`
4. Registrar acceso físico con `POST /api/v1/accesos/entrada` (requiere cédula y membresía vigente)
5. Crear reserva con `POST /api/v1/reservas`
6. Registrar venta con `POST /api/v1/ventas`

---

## 🔗 Repositorio

[https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852](https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852)