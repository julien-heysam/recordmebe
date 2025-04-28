from sqlalchemy import Column, Float, ForeignKey, JSONB, String

from src.db.db import Base
from src.db.base import BaseColumns


class RecordingTable(BaseColumns, Base):
    __tablename__ = "recording"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("org.id"), index=True)
    deal_id = Column(String, ForeignKey("deal.id"), index=True, nullable=True)

    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    participants = Column(JSONB, nullable=True)
    video_path = Column(String, nullable=True)
    duration = Column(Float, nullable=True)
