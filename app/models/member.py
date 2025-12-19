from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    membership_number = Column(String(50), unique=True, nullable=False)
    status = Column(Enum("active", "suspended"), default="active")
