"""Configuration placeholders for the application under `src/app`.

Use `pydantic.BaseSettings` to load from environment variables in future.
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "url-shortener"
    debug: bool = True
    # Database URL for SQLAlchemy / Alembic. In production set via env var.
    database_url: str = "postgresql://user:password@localhost:5432/url_shortener"


settings = Settings()
