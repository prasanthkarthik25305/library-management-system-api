from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.schemas.book_schema import BookCreate, BookResponse
from app.services.state_machine import send_book_to_maintenance

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=list[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@router.get("/available", response_model=list[BookResponse])
def get_available_books(db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.status == "available").all()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}/maintenance")
def move_to_maintenance(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    send_book_to_maintenance(db, book)
    return {"message": "Book sent to maintenance"}
