from fastapi import FastAPI
from sqlalchemy import text

from src.app.api.urls import router as urls_router
from src.app.core.config import settings
from src.app.db.session import engine


app = FastAPI(title=settings.app_name)


app.include_router(urls_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
