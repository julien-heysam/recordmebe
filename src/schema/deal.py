from typing import Optional

from src.constants import Statues
from src.schema.base import BaseSchema


class DealSchema(BaseSchema):
    org_id: Optional[str] = None

    name: str
    status: Statues = Statues.ACTIVE.value
    domain: Optional[str] = None

    def set_id(self):
        self.id = self.name
