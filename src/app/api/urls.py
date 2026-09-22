from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.app import services
from src.app.db.session import get_db
from src.app.schemas import ShortURLCreate, ShortURLResponse


router = APIRouter(
    prefix="/urls",
    tags=["urls"],
)


def build_short_url_response(
    short_url,
    request: Request,
):
    """
    Convert a ShortURL database model into the API response.

    The short_url field contains the full public URL that users
    can visit to be redirected to the original target URL.
    """

    return {
        "id": short_url.id,
        "alias": short_url.alias,
        "target_url": short_url.target_url,
        "short_url": str(
            request.url_for(
                "redirect_alias",
                alias=short_url.alias,
            )
        ),
        "click_count": short_url.click_count,
        "created_at": short_url.created_at,
    }


@router.post(
    "/shorten",
    response_model=ShortURLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    payload: ShortURLCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    # If a custom alias was supplied, make sure it is available.
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

        return build_short_url_response(
            short_url,
            request,
        )

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
    request: Request,
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

    return build_short_url_response(
        short_url,
        request,
    )


@router.get(
    "/{alias}",
    status_code=status.HTTP_302_FOUND,
)
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

    # Record the visit before redirecting.
    services.record_click(
        db,
        alias,
    )

    return RedirectResponse(
        url=short_url.target_url,
        status_code=status.HTTP_302_FOUND,
    )