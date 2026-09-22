"""ORM model for shortened URLs (relocated to `src/app/models`)."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, Text
from ..db.session import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String(128), unique=True, index=True, nullable=False)
    target_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    click_count = Column(Integer, default=0)
