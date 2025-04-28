from typing import Optional

from src.constants import Statues
from src.schema.base import BaseSchema


class OrgSchema(BaseSchema):
    name: str
    status: Statues = Statues.ACTIVE.value
    domains: Optional[list[str]] = []

    def set_id(self):
        self.id = self.name
