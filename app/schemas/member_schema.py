from pydantic import BaseModel
from pydantic import ConfigDict

class MemberCreate(BaseModel):
    name: str
    email: str
    membership_number: str


class MemberResponse(MemberCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
