from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.transaction import Transaction
from app.models.fine import Fine
from app.models.member import Member

MAX_BORROW_LIMIT = 3

# -------------------------------------------------
# 1️⃣ CHECK ACTIVE BORROW COUNT (MAX 3)
# -------------------------------------------------

def has_reached_borrow_limit(db: Session, member_id: int) -> bool:
    """
    A member cannot borrow more than 3 books simultaneously
    """
    active_borrows = (
        db.query(Transaction)
        .filter(
            Transaction.member_id == member_id,
            Transaction.status.in_(["active", "overdue"])
        )
        .count()
    )

    return active_borrows >= MAX_BORROW_LIMIT


# -------------------------------------------------
# 2️⃣ CHECK UNPAID FINES
# -------------------------------------------------

def has_unpaid_fines(db: Session, member_id: int) -> bool:
    """
    A member with unpaid fines cannot borrow books
    """
    unpaid_fines = (
        db.query(Fine)
        .filter(
            Fine.member_id == member_id,
            Fine.paid_at.is_(None)
        )
        .count()
    )

    return unpaid_fines > 0


# -------------------------------------------------
# 3️⃣ MEMBER STATUS CHECK
# -------------------------------------------------

def is_member_active(member: Member) -> bool:
    """
    Only active members are allowed to borrow books
    """
    return member.status == "active"


# -------------------------------------------------
# 4️⃣ SUSPEND MEMBER (WHEN RULES VIOLATED)
# -------------------------------------------------

def suspend_member(db: Session, member: Member):
    """
    Suspend member if business rules are violated
    """
    if member.status != "suspended":
        member.status = "suspended"
        db.commit()
        db.refresh(member)


# -------------------------------------------------
# 5️⃣ MAIN BORROW VALIDATION (USED BY API)
# -------------------------------------------------

def validate_member_can_borrow(db: Session, member: Member):
    """
    Centralized borrow validation logic
    """
    if not is_member_active(member):
        raise Exception("Member is suspended and cannot borrow books")

    if has_unpaid_fines(db, member.id):
        raise Exception("Member has unpaid fines")

    if has_reached_borrow_limit(db, member.id):
        raise Exception("Borrowing limit exceeded (max 3 books)")
