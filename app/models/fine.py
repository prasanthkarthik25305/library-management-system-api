from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL
from app.database import Base

class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    paid_at = Column(DateTime)
