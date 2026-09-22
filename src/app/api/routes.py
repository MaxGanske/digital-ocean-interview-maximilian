"""Route stubs for the URL Shortener API (moved to `src/app`)."""

from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.post("/shorten")
def create_short_url():
    """Create a shortened URL (auto-generated or user-defined alias).

    TODO: accept payload with `target_url` and optional `custom_alias`. Validate
    input, ensure alias uniqueness, persist metadata, and return created resource.
    """
    raise NotImplementedError


@router.get("/{alias}")
def redirect_alias(alias: str):
    """Redirect to the original URL for the provided alias.

    TODO: resolve alias, update click metadata, and return a 307 redirect.
    """
    raise NotImplementedError


@router.get("/meta/{alias}")
def get_metadata(alias: str):
    """Return metadata for the provided alias.

    TODO: return creation time, target URL, click-count, creator (if any), expiry.
    """
    raise NotImplementedError
