from abc import abstractmethod
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: str = None

    meta: Optional[dict] = dict()
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.set_id()

    @abstractmethod
    def set_id(self):
        ...

    class Config:
        from_attributes = True
        use_enum_values = True
        extra = "allow"
