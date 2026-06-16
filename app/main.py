from fastapi import FastAPI
from app.api.database.session import Base, engine, create_tables
from app.api.v1.routers import router as api_router

app = FastAPI(title="SmartGym API")

create_tables()

app.include_router(api_router, prefix="/api/v1")