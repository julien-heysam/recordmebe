from sqlalchemy import Column, String

from src.db.db import Base
from src.db.base import BaseColumns


class OrgTable(BaseColumns, Base):
    __tablename__ = "org"

    id = Column(String, primary_key=True)

    name = Column(String)
    status = Column(String)
    domains = Column(String, nullable=True)
