import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from src.app.api.urls import router as urls_router
from src.app.core.config import settings
from src.app.db.init_db import create_database_tables
from src.app.db.session import engine


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting application and ensuring database tables exist")
    await create_database_tables()
    logger.info("Application startup complete")
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(urls_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db", tags=["health"])
async def database_health() -> dict[str, str]:
    def _check_db() -> None:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    await asyncio.to_thread(_check_db)
    logger.info("Database health check passed")
    return {"status": "ok"}