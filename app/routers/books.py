from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter


from app.models import Book
from app.schemas import BookCreate, BookResponse, BookUpdate
from app.database import get_db

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get('/search', summary="search books by title or author", response_model=list[BookResponse])
def filter_books(
    db: Annotated[Session, Depends(get_db)],
    search: str,
) -> list[BookResponse]:
    print('this function is calling 2')

    query = db.query(Book)
    if search is not None:
        query = query.filter(Book.title.ilike(f"%{search}%") | Book.author.ilike(f"%{search}%"))

    return query.all()


@router.get('/filter', summary="filter books by year range", response_model=list[BookResponse])
def filter_books_by_year(
    db: Annotated[Session, Depends(get_db)],
    start_year: Annotated[datetime | None, None] = None,
    end_year: Annotated[datetime | None, None] = None,
) -> list[BookResponse]:
    print('this function is calling')
    query = db.query(Book)
    
    if start_year is not None:
        query = query.filter(Book.year >= start_year)
    if end_year is not None:
        query = query.filter(Book.year <= end_year)

    return query.all()


@router.post("/", summary="Add a new book", response_model=BookResponse)
def add_book(book: BookCreate, db: Annotated[Session, Depends(get_db)]) -> BookResponse:
    
    exists_book = db.query(Book).filter(Book.title == book.title).first()
    if exists_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this title already exists.",
        )
        
    new_book = Book(
        title = book.title,
        author = book.author,
        genre = book.genre,
        year = book.year,
        rating = book.rating
    )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.put('/{pk}', summary="Update an existing book", response_model=BookResponse)
def update_book(
    pk: int, 
    book: BookUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> BookResponse:
    
    existing_book = db.query(Book).filter(Book.id == pk).first()
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )
    
    existing_book.title = book.title or existing_book.title
    existing_book.author = book.author or existing_book.author
    existing_book.genre = book.genre or existing_book.genre
    existing_book.year = book.year or existing_book.year
    existing_book.rating = book.rating or existing_book.rating
    
    db.commit()
    db.refresh(existing_book)
    return existing_book


@router.get("/", summary="Get all books", response_model=list[BookResponse])
def get_books(
    db: Annotated[Session, Depends(get_db)]
) -> list[BookResponse]:
    books = db.query(Book).all()

    return books


@router.get("/{pk}", summary="Get a book by ID", response_model=BookResponse)
def get_book(
    pk: int,
    db: Annotated[Session, Depends(get_db)]
) -> BookResponse:
    book = db.query(Book).filter(Book.id == pk).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )
    return book


@router.delete("/{pk}", summary="Delete a book")
def delete_book(
    pk: int,
    db: Annotated[Session, Depends(get_db)]
):
    existing_book = db.query(Book).filter(Book.id==pk).first()
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )
    
    db.delete(existing_book)
    db.commit()
    return {"detail": "Book deleted successfully."}


