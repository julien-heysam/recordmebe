from sqlalchemy import Column, ForeignKey, String

from src.db.db import Base
from src.db.base import BaseColumns


class DealTable(BaseColumns, Base):
    __tablename__ = "deal"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("org.id"), index=True)

    name = Column(String)
    status = Column(String)
    domain = Column(String, nullable=True)
