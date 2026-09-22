"""Small helper to create tables for local/dev usage.

Run locally after Postgres is available:

    python -m src.app.db.init_db

Or include it in a deploy/run command to ensure tables exist before starting.
"""
from src.app.db import models  # noqa: F401 ensures model modules are imported
from src.app.db.session import Base, engine


def init_db() -> None:
    """Create all tables declared on the SQLAlchemy `Base` metadata."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()


async def create_database_tables() -> None:
    """Async wrapper that creates tables on a thread to avoid blocking the event loop.

    Use this from FastAPI startup lifespans, e.g.:

        await create_database_tables()

    """
    import asyncio


    await asyncio.to_thread(Base.metadata.create_all, engine)
