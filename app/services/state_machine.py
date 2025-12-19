from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.transaction import Transaction
from app.models.fine import Fine

# ------------------ CONSTANTS ------------------

LOAN_DAYS = 14
FINE_PER_DAY = 0.50
MAX_BORROW_LIMIT = 3

# ------------------ BOOK STATE MACHINE ------------------

def borrow_book(db: Session, book: Book):
    """
    available -> borrowed
    """
    if book.status != "available":
        raise Exception("Book is not available for borrowing")

    if book.available_copies <= 0:
        raise Exception("No copies available")

    book.status = "borrowed"
    book.available_copies -= 1

    db.commit()
    db.refresh(book)


def return_book(db: Session, book: Book):
    """
    borrowed/overdue -> available
    """
    if book.status not in ["borrowed", "overdue"]:
        raise Exception("Book cannot be returned in current state")

    book.available_copies += 1

    if book.available_copies > 0:
        book.status = "available"

    db.commit()
    db.refresh(book)


def send_book_to_maintenance(db: Session, book: Book):
    """
    available -> maintenance
    """
    if book.status != "available":
        raise Exception("Only available books can be sent to maintenance")

    book.status = "maintenance"
    db.commit()
    db.refresh(book)

# ------------------ TRANSACTION STATE MACHINE ------------------

def create_transaction(db: Session, book_id: int, member_id: int):
    """
    Create new borrowing transaction
    """
    borrowed_at = datetime.utcnow()
    due_date = borrowed_at + timedelta(days=LOAN_DAYS)

    transaction = Transaction(
        book_id=book_id,
        member_id=member_id,
        borrowed_at=borrowed_at,
        due_date=due_date,
        status="active"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def return_transaction(db: Session, transaction: Transaction):
    """
    active/overdue -> returned
    """
    if transaction.status not in ["active", "overdue"]:
        raise Exception("Transaction already closed")

    transaction.status = "returned"
    transaction.returned_at = datetime.utcnow()

    db.commit()
    db.refresh(transaction)


def mark_transaction_overdue(db: Session, transaction: Transaction):
    """
    active -> overdue
    """
    if transaction.status != "active":
        return

    if datetime.utcnow() > transaction.due_date:
        transaction.status = "overdue"
        db.commit()
        db.refresh(transaction)

# ------------------ FINE CALCULATION ------------------

def calculate_and_create_fine(db: Session, transaction: Transaction):
    """
    Create fine for overdue transaction
    """
    if transaction.status != "overdue":
        return None

    overdue_days = (datetime.utcnow() - transaction.due_date).days

    if overdue_days <= 0:
        return None

    fine_amount = overdue_days * FINE_PER_DAY

    fine = Fine(
        member_id=transaction.member_id,
        transaction_id=transaction.id,
        amount=fine_amount
    )

    db.add(fine)
    db.commit()
    db.refresh(fine)

    return fine
