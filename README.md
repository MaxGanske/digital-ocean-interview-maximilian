# URL Shortener (FastAPI) — Skeleton

This repository contains a skeleton for a URL shortener REST API using FastAPI. It is intentionally minimal and contains placeholders only — no production business logic yet.

Next steps:
- Implement persistence (Postgres, Redis, or SQLite) and migrations.
- Implement short-code generation and custom alias handling.
- Add redirect endpoint and metadata endpoints.
- Add tests, CI, and Docker packaging.

Run (development):

```bash
# Using Poetry (recommended)
poetry install
poetry run uvicorn src.app.main:app --reload --port 8000

# Or with Docker Compose
cp .env.example .env
docker compose up --build
```

Files of interest:
- `requirements.txt` — dependency manifest
- `app/main.py` — FastAPI app entrypoint (placeholder)
- `app/api/routes.py` — API route stubs
- `app/core/config.py` — configuration placeholder
- `tests/` — test scaffold
