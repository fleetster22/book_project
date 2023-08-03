from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    category: str
    synopsis: str
    rating: float
    img_url: str

    def __init__(
        self,
        id,
        title,
        author,
        category,
        synopsis,
        rating,
        img_url,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.synopsis = synopsis
        self.rating = rating
        self.img_url = img_url


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="id is optional")
    title: str = Field(..., min_length=1, max_length=50)
    author: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=50)
    synopsis: str = Field(..., min_length=1, max_length=500)
    rating: int = Field(..., ge=0, le=5)
    img_url: str = Field(..., min_length=1, max_length=200)

    # values of the config class are used as placeholders for the example
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Title of Book",
                "author": "Author Name(s)",
                "category": "Genre",
                "synopsis": "Description",
                "rating": 5,
                "img_url": "https://#",
            }
        }


BOOKS = [
    Book(
        1,
        "The Hobbit",
        "J.R.R. Tolkien",
        "Fantasy",
        "Bilbo Baggins, a hobbit, is smoking in his porchway one day when Gandalf the Wizard visits him. He wants Bilbo to help a group of dwarves take back the Mountain from Smaug, a dragon. Bilbo is unsure, but agrees after Gandalf promises him a share of the treasure.",
        5,
        "https://images-na.ssl-images-amazon.com/images/I/91bq+Xn1CwL.jpg",
    ),
    Book(
        2,
        "The Fellowship of the Ring",
        "J.R.R. Tolkien",
        "Fantasy",
        "The story begins in the Shire, where the hobbit Frodo Baggins inherits the Ring from Bilbo Baggins, his cousin and guardian. Neither hobbit is aware of the Ring's nature, but Gandalf the Grey, a wizard and an old friend of Bilbo, suspects it to be Sauron's Ring. Seventeen years later, after Gandalf confirms his guess, he tells Frodo the history of the Ring and counsels him to take it away from the Shire. Frodo sets out, accompanied by his gardener and friend, Samwise Gamgee, and two cousins, Meriadoc Brandybuck, called Merry, and Peregrin Took, called Pippin. They are nearly caught by the Black Riders, but shake off their pursuers by cutting through the Old Forest.",
        4,
        "https://images-na.ssl-images-amazon.com/images/I/91bq+Xn1CwL.jpg",
    ),
]


@app.get("/books")
async def get_books():
    return BOOKS


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    # model_dump is new version of dictionary, below transforms request into dictionary
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


# fastapi will automatically assign the book id
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
