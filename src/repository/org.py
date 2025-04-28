import logging

from sqlalchemy.orm import Session

from src.db import OrgTable
from src.repository.base import BaseRepository
from src.schema.org import OrgSchema

logger = logging.getLogger(__name__)


class OrgRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, OrgSchema, OrgTable)
