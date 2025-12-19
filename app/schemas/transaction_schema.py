from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime

class TransactionResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: datetime | None
    status: str

    model_config = ConfigDict(from_attributes=True)