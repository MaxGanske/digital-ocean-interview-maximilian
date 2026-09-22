# URL Shortener (FastAPI) — Skeleton

This repository contains a compact interview-ready skeleton for a URL shortening API built with FastAPI, SQLAlchemy and PostgreSQL.

Next steps:
- Implement persistence (Postgres, Redis, or SQLite) and migrations.
- Implement short-code generation and custom alias handling.
- Add redirect endpoint and metadata endpoints.
- Add tests, CI, and Docker packaging.

Run (development):

Project layout (important paths):

- [src/app/main.py](src/app/main.py#L1) — FastAPI application entrypoint
- [src/app/api/urls.py](src/app/api/urls.py#L1) — API route stubs
- [src/app/services.py](src/app/services.py#L1) — business/service layer (TODO)
- [src/app/schemas.py](src/app/schemas.py#L1) — Pydantic request/response models
- [src/app/core/config.py](src/app/core/config.py#L1) — configuration (pydantic-settings)
- [src/app/db/session.py](src/app/db/session.py#L1) — SQLAlchemy engine / session
- [src/app/db/models.py](src/app/db/models.py#L1) — ORM models
- [tests/](tests/) — basic test scaffolding

Local development

1. Copy the example env file (keeps secrets out of VCS):

```bash
cp .env.example .env
```

2. Start Postgres (OrbStack / Docker Compose):

```bash
docker compose up -d postgres
```

3. Install dependencies (Poetry):

```bash
poetry install
```

4. Run the API locally:

```bash
poetry run uvicorn src.app.main:app --reload --port 8000
```

5. Run tests:

```bash
poetry run pytest -q
```

Health checks

- Application: `GET /health` — returns `{"status": "ok"}`
- Database: `GET /health/db` — runs a `SELECT 1` against the configured DB

Notes and small fixes applied

- Paths updated to `src/app/` (previous README referenced older `app/` paths).
- `compose.yml` is the Compose file in the repo (README references `docker compose` which is compatible).
- `pydantic-settings` is used in `src/app/core/config.py` to support Pydantic v2 settings.
- No `.pre-commit-config.yaml` was found in the repo so no pre-commit changes were required.

What to do next (suggested)

- Implement the create/redirect flow in `src/app/services.py` and wire it through `src/app/api/urls.py`.
- Add migrations (Alembic) if you want persisted schema evolution.

That's it — the skeleton is ready for the interview workflow: implement the TODOs in `services.py` and `urls.py`.
