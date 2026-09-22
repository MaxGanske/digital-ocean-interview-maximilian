from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from src.app import services
from src.app.db.models import ShortURL
from src.app.schemas import ShortURLCreate


def test_generate_alias_default_length():
    alias = services.generate_alias()

    assert len(alias) == services.ALIAS_LENGTH


def test_generate_alias_custom_length():
    alias = services.generate_alias(10)

    assert len(alias) == 10


def test_generate_alias_contains_only_valid_characters():
    alias = services.generate_alias()

    for character in alias:
        assert character in services.ALIAS_CHARACTERS


def test_get_url_by_alias_returns_url():
    db = MagicMock()

    expected_url = ShortURL(
        alias="google",
        target_url="https://google.com",
    )

    db.query.return_value.filter.return_value.first.return_value = expected_url

    result = services.get_url_by_alias(
        db,
        "google",
    )

    assert result == expected_url

    db.query.assert_called_once_with(ShortURL)
    db.query.return_value.filter.return_value.first.assert_called_once()


def test_get_url_by_alias_returns_none_when_missing():
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    result = services.get_url_by_alias(
        db,
        "missing",
    )

    assert result is None


def test_create_short_url_with_custom_alias(monkeypatch):
    db = MagicMock()

    payload = ShortURLCreate(
        target_url="https://example.com",
        custom_alias="example",
    )

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: None,
    )

    result = services.create_short_url(
        db,
        payload,
    )

    assert result.alias == "example"
    assert result.target_url == "https://example.com/"

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)


def test_create_short_url_with_duplicate_custom_alias(
    monkeypatch,
):
    db = MagicMock()

    payload = ShortURLCreate(
        target_url="https://example.com",
        custom_alias="taken",
    )

    existing_url = ShortURL(
        alias="taken",
        target_url="https://other.com",
    )

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: existing_url,
    )

    with pytest.raises(
        ValueError,
        match="Alias already exists",
    ):
        services.create_short_url(
            db,
            payload,
        )

    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_create_short_url_generates_alias_when_not_provided(
    monkeypatch,
):
    db = MagicMock()

    payload = ShortURLCreate(
        target_url="https://example.com",
    )

    monkeypatch.setattr(
        services,
        "generate_alias",
        lambda: "abc1234",
    )

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: None,
    )

    result = services.create_short_url(
        db,
        payload,
    )

    assert result.alias == "abc1234"
    assert result.target_url == "https://example.com/"

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)


def test_generated_alias_collision_generates_new_alias(
    monkeypatch,
):
    db = MagicMock()

    payload = ShortURLCreate(
        target_url="https://example.com",
    )

    aliases = iter(
        [
            "taken12",
            "free123",
        ]
    )

    monkeypatch.setattr(
        services,
        "generate_alias",
        lambda: next(aliases),
    )

    def fake_get_url_by_alias(db, alias):
        if alias == "taken12":
            return ShortURL(
                alias="taken12",
                target_url="https://existing.com",
            )

        return None

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        fake_get_url_by_alias,
    )

    result = services.create_short_url(
        db,
        payload,
    )

    assert result.alias == "free123"

    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_create_short_url_rolls_back_on_integrity_error(
    monkeypatch,
):
    db = MagicMock()

    payload = ShortURLCreate(
        target_url="https://example.com",
        custom_alias="example",
    )

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: None,
    )

    db.commit.side_effect = IntegrityError(
        statement="INSERT",
        params={},
        orig=Exception("duplicate"),
    )

    with pytest.raises(
        ValueError,
        match="Alias already exists",
    ):
        services.create_short_url(
            db,
            payload,
        )

    db.rollback.assert_called_once()


def test_record_click_increments_click_count(
    monkeypatch,
):
    db = MagicMock()

    short_url = ShortURL(
        alias="example",
        target_url="https://example.com",
        click_count=0,
    )

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: short_url,
    )

    result = services.record_click(
        db,
        "example",
    )

    assert result.click_count == 1

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(short_url)


def test_record_click_existing_count(
    monkeypatch,
):
    db = MagicMock()

    short_url = ShortURL(
        alias="example",
        target_url="https://example.com",
        click_count=10,
    )

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: short_url,
    )

    result = services.record_click(
        db,
        "example",
    )

    assert result.click_count == 11


def test_record_click_returns_none_when_alias_missing(
    monkeypatch,
):
    db = MagicMock()

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: None,
    )

    result = services.record_click(
        db,
        "missing",
    )

    assert result is None

    db.commit.assert_not_called()
    db.refresh.assert_not_called()