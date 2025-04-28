from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import UTC_TIMESTAMP


class BaseColumns:
    """Mixin that adds common columns to all tables"""

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime(timezone=True), server_default=UTC_TIMESTAMP)
    updated_at = Column(DateTime(timezone=True), server_default=UTC_TIMESTAMP, onupdate=UTC_TIMESTAMP)
