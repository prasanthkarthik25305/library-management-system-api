from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member import Member
from app.models.transaction import Transaction
from app.schemas.member_schema import MemberCreate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/", response_model=list[MemberResponse])
def get_all_members(db: Session = Depends(get_db)):
    return db.query(Member).all()


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.get("/{member_id}/borrowed")
def get_borrowed_books(member_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Transaction)
        .filter(
            Transaction.member_id == member_id,
            Transaction.status.in_(["active", "overdue"])
        )
        .all()
    )
