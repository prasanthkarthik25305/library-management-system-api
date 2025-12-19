from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    category = Column(String(100))
    status = Column(
        Enum("available", "borrowed", "reserved", "maintenance"),
        default="available"
    )
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
