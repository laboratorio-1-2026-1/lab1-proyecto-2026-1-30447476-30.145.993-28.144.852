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
├── 🌐 api/          # Controladores — Rutas y validación de entrada
├── 💼 domain/       # Servicios — Lógica de negocio
└── 🗄️ infrastructure/  # Repositorios — Comunicación con PostgreSQL
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

## ⚙️ Instalación y Uso

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

### 4. Configurar la base de datos
El proyecto puede usar SQLite por defecto con `sqlite:///./smartgym.db`.
Si deseas conectar PostgreSQL, define `DATABASE_URL` en el entorno o en un archivo `.env`.

Ejemplo de variable de entorno (PowerShell):
```powershell
$env:DATABASE_URL = 'postgresql://postgres:password@localhost:5432/smartgym_db'
```

### 5. Poblar la base de datos con datos de prueba
Ejecuta el seeder para crear roles, usuarios, máquinas, productos, planes y datos de prueba.

```bash
python -m app.api.database.seeders
```

Al ejecutar el seeder se crearán usuarios iniciales, incluyendo:

- `admin@smartgym.com` / `Admin2026!`  — Administrador
- `finanzas@smartgym.com` / `Finanzas2026!`  — Finanzas
- `carlos@smartgym.com` / `Entrenador2026!`  — Entrenador
- `laura@smartgym.com` / `Entrenador2026!`  — Entrenador
- `maria@gmail.com` / `Cliente2026!`  — Cliente
- `pedro@gmail.com` / `Cliente2026!`  — Cliente
- `ana@gmail.com` / `Cliente2026!`  — Cliente

### 6. Ejecutar localmente con Uvicorn
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 7. Probar endpoints desde Swagger
1. Abre Swagger UI en: `http://127.0.0.1:8000/docs`
2. Usa el botón `Try it out` en `/api/v1/auth/login`.
3. Envía el cuerpo JSON con credenciales, por ejemplo:
```json
{
  "email": "admin@smartgym.com",
  "password": "Admin2026!"
}
```
4. Copia el valor de `token` de la respuesta.
5. Haz clic en el botón `Authorize` en Swagger e ingresa:
```
Bearer <token>
```
6. Ahora puedes probar cualquier endpoint protegido, por ejemplo:
   - `/api/v1/auth/me`
   - `/api/v1/pagos`
   - `/api/v1/reservas`
   - `/api/v1/usuarios`

### 8. Secuencia recomendada de pruebas
1. Crear un usuario nuevo con `/api/v1/auth/register` (opcional).
2. Iniciar sesión con `/api/v1/auth/login`.
3. Usar el token devuelto para autorizar requests protegidos.
4. Probar un endpoint protegido, por ejemplo `/api/v1/auth/me`.

> Nota: también puedes ejecutar las mismas llamadas con `curl` si prefieres no usar Swagger.

---

## 📖 Documentación

Una vez ejecutada la API, accede a la documentación interactiva en:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔗 Repositorio

[https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852](https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852)