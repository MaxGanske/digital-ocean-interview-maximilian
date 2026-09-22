"""SQLAlchemy engine, session, and base declarative for the project (src/app)."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings


# Use DATABASE_URL from settings (set via env var in production)
DATABASE_URL = settings.database_url

# create engine (Postgres expected in production)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base for models
Base = declarative_base()


def get_db():
    """Yield a database session and ensure it's closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
