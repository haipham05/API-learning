from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str 
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(min_length=4)

    model_config = {
        "json_schema_extra": {
            "example": {
                'title': 'A new book',
                'author': 'HaiPham',
                'description': 'A description',
                'rating': 5,
                'published_date': 2013
            }
        }
    }

BOOKS = [
    Book(1, "Comp-Sci", "Hai Pham", "Comp-Sci fundamental", 5, 2013),
    Book(2, "AI don gian", "Hai Pham", "very gud book", 5, 2011),
    Book(3, "The Lord of the Rings", "J.R.R.Tolkien", "peak fantasy novel", 5, 1937),
    Book(4, "God Father", "Mario Puzo", "Great book", 5, 1969),
    Book(5, "Toi thay hoa vang tren co xanh", "Nguyen Nhat Anh", "good book to read", 4, 2010),
    Book(6, "Rich Dad Poor Dad", "Robert T.Kiyosaki", "groundbreaking personal finance book", 4, 1997),
]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/by_id/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get("/books/")
async def read_book_by_rating(rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
    
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    newbook = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(newbook))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
    
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break

@app.get("/books/by_date/{published_date}")
async def read_book_by_published_date(published_date: int):
    book_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            book_to_return.append(BOOKS[i])
    return book_to_return