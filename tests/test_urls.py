from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.app import services
from src.app.db.models import ShortURL
from src.app.db.session import get_db
from src.app.api.urls import router


app = FastAPI()

app.include_router(router)


fake_db = MagicMock()


def override_get_db():
    yield fake_db


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_mocks():
    fake_db.reset_mock()


def make_short_url(
    alias="example",
    target_url="https://example.com/",
    click_count=0,
):
    return ShortURL(
        id=1,
        alias=alias,
        target_url=target_url,
        click_count=click_count,
        created_at=datetime.now(timezone.utc),
    )


def test_create_short_url_with_custom_alias(
    monkeypatch,
):
    short_url = make_short_url()

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: None,
    )

    monkeypatch.setattr(
        services,
        "create_short_url",
        lambda db, payload: short_url,
    )

    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "https://example.com",
            "custom_alias": "example",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["alias"] == "example"
    assert data["target_url"] == "https://example.com/"
    assert data["short_url"] == "http://testserver/urls/example"
    assert data["click_count"] == 0
    assert data["created_at"] is not None


def test_create_short_url_without_custom_alias(
    monkeypatch,
):
    short_url = make_short_url(
        alias="abc1234",
    )

    monkeypatch.setattr(
        services,
        "create_short_url",
        lambda db, payload: short_url,
    )

    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "https://example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["alias"] == "abc1234"
    assert data["short_url"] == "http://testserver/urls/abc1234"


def test_create_short_url_invalid_url():
    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "not-a-url",
        },
    )

    assert response.status_code == 422


def test_create_short_url_missing_target_url():
    response = client.post(
        "/urls/shorten",
        json={},
    )

    assert response.status_code == 422


def test_custom_alias_too_short():
    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "https://example.com",
            "custom_alias": "ab",
        },
    )

    assert response.status_code == 422


def test_custom_alias_too_long():
    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "https://example.com",
            "custom_alias": "a" * 33,
        },
    )

    assert response.status_code == 422


def test_custom_alias_invalid_characters():
    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "https://example.com",
            "custom_alias": "hello world",
        },
    )

    assert response.status_code == 422


def test_duplicate_alias_returns_409(
    monkeypatch,
):
    existing_url = make_short_url()

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: existing_url,
    )

    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "https://example.com",
            "custom_alias": "example",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "Alias already exists",
    }


def test_service_value_error_returns_400(
    monkeypatch,
):
    monkeypatch.setattr(
        services,
        "create_short_url",
        MagicMock(
            side_effect=ValueError(
                "Unable to create URL"
            )
        ),
    )

    response = client.post(
        "/urls/shorten",
        json={
            "target_url": "https://example.com",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Unable to create URL",
    }


def test_get_url_metadata(
    monkeypatch,
):
    short_url = make_short_url(
        click_count=3,
    )

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: short_url,
    )

    response = client.get(
        "/urls/meta/example",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["alias"] == "example"
    assert data["target_url"] == "https://example.com/"
    assert data["short_url"] == "http://testserver/urls/example"
    assert data["click_count"] == 3


def test_get_url_metadata_missing_returns_404(
    monkeypatch,
):
    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: None,
    )

    response = client.get(
        "/urls/meta/missing",
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Short URL not found",
    }


def test_redirect_returns_302(
    monkeypatch,
):
    short_url = make_short_url()

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: short_url,
    )

    monkeypatch.setattr(
        services,
        "record_click",
        lambda db, alias: short_url,
    )

    response = client.get(
        "/urls/example",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        response.headers["location"]
        == "https://example.com/"
    )


def test_redirect_missing_alias_returns_404(
    monkeypatch,
):
    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: None,
    )

    response = client.get(
        "/urls/missing",
        follow_redirects=False,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Short URL not found",
    }


def test_redirect_records_click(
    monkeypatch,
):
    short_url = make_short_url()

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: short_url,
    )

    record_click = MagicMock(
        return_value=short_url,
    )

    monkeypatch.setattr(
        services,
        "record_click",
        record_click,
    )

    response = client.get(
        "/urls/example",
        follow_redirects=False,
    )

    assert response.status_code == 302

    record_click.assert_called_once_with(
        fake_db,
        "example",
    )


def test_metadata_does_not_record_click(
    monkeypatch,
):
    short_url = make_short_url()

    monkeypatch.setattr(
        services,
        "get_url_by_alias",
        lambda db, alias: short_url,
    )

    record_click = MagicMock()

    monkeypatch.setattr(
        services,
        "record_click",
        record_click,
    )

    response = client.get(
        "/urls/meta/example",
    )

    assert response.status_code == 200

    record_click.assert_not_called()