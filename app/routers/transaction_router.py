from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.member import Member
from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionResponse

from app.services.state_machine import (
    borrow_book,
    return_book,
    create_transaction,
    return_transaction,
    mark_transaction_overdue,
    calculate_and_create_fine
)

from app.services.business_rules import validate_member_can_borrow

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/borrow", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def borrow_book_api(
    book_id: int,
    member_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(Book).get(book_id)
    member = db.query(Member).get(member_id)

    if not book or not member:
        raise HTTPException(status_code=404, detail="Book or Member not found")

    try:
        validate_member_can_borrow(db, member)
        borrow_book(db, book)
        transaction = create_transaction(db, book.id, member.id)
        return transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{transaction_id}/return")
def return_book_api(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    book = db.query(Book).get(transaction.book_id)

    try:
        mark_transaction_overdue(db, transaction)
        calculate_and_create_fine(db, transaction)
        return_transaction(db, transaction)
        return_book(db, book)
        return {"message": "Book returned successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/overdue")
def get_overdue_transactions(db: Session = Depends(get_db)):
    return (
        db.query(Transaction)
        .filter(Transaction.status == "overdue")
        .all()
    )
