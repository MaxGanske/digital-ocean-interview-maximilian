"""FastAPI application entrypoint (skeleton) located in `src/app`."""

from fastapi import FastAPI
from .api.routes import router as api_router

app = FastAPI(title="URL Shortener (skeleton)")


@app.get("/")
def root():
    """Health / placeholder endpoint."""
    return {"status": "skeleton", "message": "Implement API endpoints in src.app.api"}


# include API routes (skeleton)
app.include_router(api_router)
