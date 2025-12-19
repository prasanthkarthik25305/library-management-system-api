from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    borrowed_at = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    returned_at = Column(DateTime)
    status = Column(Enum("active", "returned", "overdue"), default="active")
