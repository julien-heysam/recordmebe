from typing import Optional
from uuid import NAMESPACE_DNS, uuid5

from pydantic import EmailStr

from src.schema.base import BaseSchema


class RecordingSchema(BaseSchema):
    org_id: Optional[str] = None

    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    participants: Optional[list[EmailStr]] = None
    video_path: Optional[str] = None
    duration: Optional[float] = None

    def set_id(self):
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_id}:{self.url}:{self.created_at}"))


if __name__ == "__main__":
    recording = RecordingSchema(org_id="org_1", url="https://www.google.com", title="Test Recording", description="Test Description", participants=["test@test.com"])
    print(recording)
    # Expected output:
    # id='46122b30-2e4d-5e5a-8fdf-2f662bd5da84' meta={} created_at=None updated_at=None org_id='org_1' url='https://www.google.com' title='Test Recording' description='Test Description' participants=['test@test.com'] video_path=None duration=None
