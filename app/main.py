from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import models
from app.models.models import Book, BookRecord, User
from app.routes import auth
from app.security import get_current_user

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookTracker API")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include auth router
app.include_router(auth.router)


# Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard")
async def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": current_user}
    )


# API endpoints
@app.get("/api/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@app.post("/api/books")
def create_book(
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(None),
    genre: str = Form(None),
    db: Session = Depends(get_db),
):
    book = Book(title=title, author=author, year=year, genre=genre)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/api/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # First, delete any associated records
    db.query(BookRecord).filter(BookRecord.book_id == book_id).delete()

    # Then delete the book
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}


@app.post("/api/records")
def create_record(
    book_id: int = Form(...),
    rating: float = Form(None),
    review: str = Form(None),
    db: Session = Depends(get_db),
):
    user = get_current_user(db)
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    record = BookRecord(user_id=user.id, book_id=book_id, rating=rating, review=review)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/api/records")
def get_records(db: Session = Depends(get_db)):
    user = get_current_user(db)
    records = db.query(BookRecord).filter(BookRecord.user_id == user.id).all()
    return records
