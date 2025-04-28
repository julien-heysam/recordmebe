import logging

from sqlalchemy.orm import Session

from src.db import RecordingTable
from src.repository.base import BaseRepository
from src.schema.recording import RecordingSchema

logger = logging.getLogger(__name__)


class RecordingRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, RecordingSchema, RecordingTable)
