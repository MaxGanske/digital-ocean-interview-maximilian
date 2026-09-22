# URL Shortener (FastAPI)

A URL shortening API built with **FastAPI, SQLAlchemy, and PostgreSQL**.

The application lets users submit a long URL and receive a shorter URL backed by a unique alias. Users may optionally provide their own custom alias. Visiting the shortened URL redirects to the original URL and increments its click count.

### Creating a shortened URL

```text
POST /urls/shorten
        ↓
Pydantic validates request
        ↓
API route
        ↓
Service layer
        ↓
Use custom alias OR generate random alias
        ↓
Check alias uniqueness
        ↓
Save URL mapping to PostgreSQL
        ↓
Return shortened URL
```

Example request:

```json
{
  "target_url": "https://www.example.com/some/really/long/path"
}
```

Example response:

```json
{
  "id": 1,
  "alias": "a7KpQ2x",
  "target_url": "https://www.example.com/some/really/long/path",
  "short_url": "https://your-app.com/urls/a7KpQ2x",
  "click_count": 0,
  "created_at": "2026-09-22T21:51:28.776676Z"
}
```

A custom alias can also be supplied:

```json
{
  "target_url": "https://www.example.com/some/really/long/path",
  "custom_alias": "example"
}
```

### Redirecting a shortened URL

```text
GET /urls/{alias}
        ↓
Find alias in PostgreSQL
        ↓
Increment click count
        ↓
302 Redirect
        ↓
Original URL
```

For example:

```text
GET /urls/a7KpQ2x
```

redirects to:

```text
https://www.example.com/some/really/long/path
```

### Retrieving metadata

```text
GET /urls/meta/{alias}
```

Returns information including:

* Alias
* Original target URL
* Full shortened URL
* Click count
* Creation time

## Project Structure

```text
src/
└── app/
    ├── main.py
    ├── schemas.py
    ├── services.py
    │
    ├── api/
    │   └── urls.py
    │
    ├── core/
    │   └── config.py
    │
    └── db/
        ├── models.py
        └── session.py

tests/
├── test_health.py
├── test_services.py
└── test_urls.py

.github/
└── workflows/
    └── ci.yml

.env.example
compose.yml
requirements.txt
pyproject.toml
requirements.md
runtime.txt
README.md
```

## Important Files

* `src/app/main.py`

  * FastAPI application entry point
  * Registers the URL router
  * Provides application and database health checks

* `src/app/api/urls.py`

  * Defines the URL-shortening HTTP endpoints
  * Handles HTTP responses, validation errors, redirects, and status codes

* `src/app/services.py`

  * Contains the main business logic
  * Generates aliases
  * Checks alias uniqueness
  * Creates shortened URLs
  * Looks up aliases
  * Records clicks

* `src/app/schemas.py`

  * Defines Pydantic request and response models
  * Validates target URLs and custom aliases

* `src/app/db/models.py`

  * Defines the SQLAlchemy `ShortURL` database model

* `src/app/db/session.py`

  * Creates the SQLAlchemy engine
  * Creates database sessions
  * Provides the FastAPI `get_db()` dependency

* `src/app/core/config.py`

  * Reads configuration from environment variables
  * Provides application and database settings

* `tests/test_services.py`

  * Unit tests for service/business logic
  * Uses mocked database sessions rather than a real database

* `tests/test_urls.py`

  * Unit tests for API behavior
  * Tests validation, status codes, redirects, and service interactions

* `.github/workflows/ci.yml`

  * Runs linting and tests automatically through GitHub Actions

## API Endpoints

### Create Short URL

```text
POST /urls/shorten
```

Request:

```json
{
  "target_url": "https://example.com",
  "custom_alias": "example"
}
```

`custom_alias` is optional. If it is not supplied, the application automatically generates an alias.

### Redirect

```text
GET /urls/{alias}
```

Looks up the alias, increments its click count, and returns a `302` redirect to the original URL.

### URL Metadata

```text
GET /urls/meta/{alias}
```

Returns the URL's stored metadata.

### Application Health

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Database Health

```text
GET /health/db
```

Runs a simple database query to verify connectivity.

Expected response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

## Local Development

### 1. Create the environment file

```bash
cp .env.example .env
```

The default local configuration is:

```env
APP_NAME=URL Shortener
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/url_shortener
```

Do not commit the real `.env` file.

### 2. Start PostgreSQL

The repository includes `compose.yml` for running PostgreSQL locally with Docker or OrbStack.

```bash
docker compose up -d
```

Verify the container is running:

```bash
docker compose ps
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
python -m uvicorn src.app.main:app --reload --port 8000
```

The API is available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

OpenAPI specification:

```text
http://localhost:8000/openapi.json
```

### 5. Run tests

```bash
python -m pytest -v
```

The unit tests do not require a live PostgreSQL database because the service and route dependencies are mocked.

### 6. Run linting

```bash
ruff check .
```

### 7. Stop local PostgreSQL

```bash
docker compose down
```

To also delete the local database volume:

```bash
docker compose down -v
```

## Testing

The project separates tests by application layer.

### Service Tests

`tests/test_services.py` tests:

* Alias generation
* Alias lookup
* Custom aliases
* Automatically generated aliases
* Alias collisions
* Duplicate aliases
* Transaction rollback behavior
* Click counting
* Missing aliases

Database behavior is mocked so these remain fast unit tests.

### API Tests

`tests/test_urls.py` tests:

* Successful URL creation
* Automatic alias creation
* Invalid URLs
* Invalid custom aliases
* Duplicate aliases
* Metadata retrieval
* Missing aliases
* Redirect responses
* Click recording
* HTTP status codes

The real FastAPI routes are exercised while the service layer is mocked.

## Continuous Integration

GitHub Actions runs CI on pushes and pull requests.

The workflow:

```text
Checkout repository
        ↓
Set up Python
        ↓
Install requirements.txt
        ↓
Run Ruff
        ↓
Run pytest
```

Because the tests use mocks, CI does not need to start a PostgreSQL service.

## DigitalOcean Deployment

The application can be deployed as a **Web Service** on DigitalOcean App Platform.

### Run Command

```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8080
```

### HTTP Port

```text
8080
```

### Environment Variables

Production configuration should be provided through DigitalOcean App Platform rather than committed to the repository.

Example:

```text
APP_NAME=URL Shortener
ENVIRONMENT=production
DATABASE_URL=<DigitalOcean PostgreSQL connection string>
```

The local `localhost:5432` database URL should not be used in DigitalOcean.

### Database

Attach a PostgreSQL database to the App Platform application and configure `DATABASE_URL` to point to it.

The deployed architecture is:

```text
Client
  ↓
DigitalOcean App Platform
  ↓
FastAPI / Uvicorn
  ↓
SQLAlchemy
  ↓
DigitalOcean PostgreSQL
```

## Scope

The current implementation intentionally keeps the architecture simple and focused.

Out of scope:

* Authentication
* User accounts
* Redis caching
* Microservices
* Distributed alias generation
* Rate limiting
* URL expiration
* Advanced analytics

These could be introduced later if scale or product requirements justified them.
