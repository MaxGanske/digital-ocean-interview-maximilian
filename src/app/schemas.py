from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ShortURLCreate(BaseModel):
    target_url: HttpUrl

    custom_alias: str | None = Field(
        default=None,
        min_length=3,
        max_length=32,
    )


class ShortURLResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    alias: str
    target_url: str
    click_count: int
    created_at: datetime