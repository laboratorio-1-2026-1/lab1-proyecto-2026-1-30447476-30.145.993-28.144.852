import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Cargar variables desde el archivo .env (buscando en la carpeta correcta)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# También intenta cargar desde el directorio actual
load_dotenv()

# Leer la URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar si se cargó
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no encontrada en el archivo .env")

# Crear motor (versión mejorada con pool)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base para modelos (solo una)
Base = declarative_base()

# Dependencia con manejo de transacciones
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


    
