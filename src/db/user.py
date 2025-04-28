from sqlalchemy import Column, ForeignKey, String

from src.db.db import Base
from src.db.base import BaseColumns


class UserTable(BaseColumns, Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("org.id"), index=True)

    name = Column(String)
    email = Column(String)
    role = Column(String)
