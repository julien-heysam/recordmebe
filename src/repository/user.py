import logging

from sqlalchemy.orm import Session

from src.db import UserTable
from src.repository.base import BaseRepository
from src.schema.user import UserSchema

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, UserSchema, UserTable)
