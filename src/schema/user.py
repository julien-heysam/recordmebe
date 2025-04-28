from typing import Optional
from uuid import NAMESPACE_DNS, uuid5

from pydantic import EmailStr

from src.schema.base import BaseSchema


class UserSchema(BaseSchema):
    org_id: Optional[str] = None

    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[str] = None

    def set_id(self):
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_id}:{self.email}"))


if __name__ == "__main__":
    user = UserSchema(org_id="org_1", email="test@test.com", name="Test User", role="admin")
    print(user)
    # Expected output:
    # id='c425f0e5-dd6c-5994-992a-c4f2413aa699' meta={} created_at=None updated_at=None org_id='org_1' email='test@test.com' name='Test User' role='admin'
