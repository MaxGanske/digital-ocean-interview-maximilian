from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.schemas import ShortURLCreate, ShortURLResponse
from src.app import services


router = APIRouter(
    prefix="/api",
    tags=["urls"],
)


@router.post(
    "/shorten",
    response_model=ShortURLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    payload: ShortURLCreate,
    db: Session = Depends(get_db),
):
    # If the user provided a custom alias, make sure it is available.
    if payload.custom_alias:
        existing_url = services.get_url_by_alias(
            db,
            payload.custom_alias,
        )

        if existing_url:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Alias already exists",
            )

    try:
        short_url = services.create_short_url(
            db,
            payload,
        )

        return short_url

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/meta/{alias}",
    response_model=ShortURLResponse,
)
def get_url_metadata(
    alias: str,
    db: Session = Depends(get_db),
):
    short_url = services.get_url_by_alias(
        db,
        alias,
    )

    if not short_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )

    return short_url


@router.get("/{alias}")
def redirect_alias(
    alias: str,
    db: Session = Depends(get_db),
):
    short_url = services.get_url_by_alias(
        db,
        alias,
    )

    if not short_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )

    # Increment click count before redirecting.
    services.record_click(
        db,
        alias,
    )

    return RedirectResponse(
        url=short_url.target_url,
        status_code=status.HTTP_302_FOUND,
    )