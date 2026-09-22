from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.schemas import ShortURLCreate, ShortURLResponse


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
    """
    TODO:
    1. Validate the request.
    2. Generate an alias if one was not provided.
    3. Make sure the alias is unique.
    4. Save the URL to PostgreSQL.
    5. Return the created URL.
    """

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="URL creation not implemented yet",
    )


@router.get(
    "/meta/{alias}",
    response_model=ShortURLResponse,
)
def get_url_metadata(
    alias: str,
    db: Session = Depends(get_db),
):
    """
    TODO:
    1. Find URL by alias.
    2. Return 404 if it does not exist.
    3. Return metadata.
    """

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Metadata lookup not implemented yet",
    )


@router.get("/{alias}")
def redirect_alias(
    alias: str,
    db: Session = Depends(get_db),
):
    """
    TODO:
    1. Find the URL by alias.
    2. Return 404 if it does not exist.
    3. Increment the click count.
    4. Redirect the user to the target URL.
    """

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Redirect not implemented yet",
    )