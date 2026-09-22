from sqlalchemy.orm import Session

from src.app.schemas import ShortURLCreate


def create_short_url(
    db: Session,
    payload: ShortURLCreate,
):
    """
    Create and store a shortened URL.

    TODO:
    - Check whether custom alias already exists.
    - Generate an alias if needed.
    - Create the database object.
    - Save it.
    - Return it.
    """

    raise NotImplementedError


def get_url_by_alias(
    db: Session,
    alias: str,
):
    """
    Find a shortened URL using its alias.

    TODO:
    - Query ShortURL by alias.
    - Return the object if found.
    - Return None if not found.
    """

    raise NotImplementedError


def record_click(
    db: Session,
    alias: str,
):
    """
    Increment the click count for a shortened URL.

    TODO:
    - Find URL by alias.
    - Increment click_count.
    - Commit the update.
    - Return the updated object.
    """

    raise NotImplementedError