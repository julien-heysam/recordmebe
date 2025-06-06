from sqlalchemy import Column, String

from src.db.base import BaseColumns
from src.db.db import Base


class OrgTable(BaseColumns, Base):
    __tablename__ = "org"

    id = Column(String, primary_key=True)

    name = Column(String)
    status = Column(String)
    domain = Column(String, nullable=True)
