from pydantic import BaseModel
from pydantic import ConfigDict

class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str
    category: str | None = None
    total_copies: int
    available_copies: int


class BookResponse(BookCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
