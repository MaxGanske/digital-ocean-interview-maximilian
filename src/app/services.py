import secrets
import string

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.app.db.models import ShortURL
from src.app.schemas import ShortURLCreate


ALIAS_LENGTH = 7
ALIAS_CHARACTERS = string.ascii_letters + string.digits


def generate_alias(length: int = ALIAS_LENGTH) -> str:
    """
    Generate a random URL-safe alias.
    """
    return "".join(
        secrets.choice(ALIAS_CHARACTERS)
        for _ in range(length)
    )


def get_url_by_alias(
    db: Session,
    alias: str,
):
    """
    Find a shortened URL by alias.

    Returns the ShortURL if found, otherwise None.
    """
    return (
        db.query(ShortURL)
        .filter(ShortURL.alias == alias)
        .first()
    )


def create_short_url(
    db: Session,
    payload: ShortURLCreate,
):
    """
    Create and store a shortened URL.
    """

    # Use the custom alias if one was provided.
    if payload.custom_alias:
        alias = payload.custom_alias

        existing_url = get_url_by_alias(
            db,
            alias,
        )

        if existing_url:
            raise ValueError("Alias already exists")

    else:
        # Generate aliases until we find one that does not exist.
        while True:
            alias = generate_alias()

            existing_url = get_url_by_alias(
                db,
                alias,
            )

            if not existing_url:
                break

    short_url = ShortURL(
        alias=alias,
        target_url=str(payload.target_url),
    )

    db.add(short_url)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise ValueError("Alias already exists")

    db.refresh(short_url)

    return short_url


def record_click(
    db: Session,
    alias: str,
):
    """
    Increment the click count for a shortened URL.

    Returns the updated ShortURL or None if it does not exist.
    """

    short_url = get_url_by_alias(
        db,
        alias,
    )

    if not short_url:
        return None

    short_url.click_count += 1

    db.commit()
    db.refresh(short_url)

    return short_url