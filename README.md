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
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Edita el archivo .env con tus credenciales de base de datos
```

### 5. Ejecutar con Docker
```bash
docker-compose up --build
```

### 6. Ejecutar localmente
```bash
uvicorn app.main:app --reload
```

---

## 📖 Documentación

Una vez ejecutada la API, accede a la documentación interactiva en:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔗 Repositorio

[https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852](https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30447476--30.145.993-28.144.852)