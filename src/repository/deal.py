import logging

from sqlalchemy.orm import Session

from src.db import DealTable
from src.repository.base import BaseRepository
from src.schema.deal import DealSchema

logger = logging.getLogger(__name__)


class DealRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, DealSchema, DealTable)
