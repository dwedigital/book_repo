from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.database import Base, engine, get_db
from app.models.models import Book, BookRecord, User
from app.routes import auth
from app.security import get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookTracker API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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


# Protected API endpoints - ALL MADE ASYNC
@app.get("/api/books")
async def get_books(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    # Get all books in the database
    books = db.query(Book).all()
    return books


@app.post("/api/books")
async def create_book(
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(None),
    genre: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    book = Book(title=title, author=author, year=year, genre=genre)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/api/books/{book_id}")
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # First check if the user has a record for this book
    records = (
        db.query(BookRecord)
        .filter(BookRecord.book_id == book_id, BookRecord.user_id == current_user.id)
        .all()
    )

    # Delete user's records for this book
    for record in records:
        db.delete(record)

    db.commit()
    return {"message": "Book removed from your collection"}


@app.post("/api/records")
async def create_record(
    book_id: int = Form(...),
    rating: float = Form(None),
    review: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if book exists
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if user already has a record for this book
    existing_record = (
        db.query(BookRecord)
        .filter(BookRecord.user_id == current_user.id, BookRecord.book_id == book_id)
        .first()
    )

    if existing_record:
        # Update existing record
        existing_record.rating = rating
        existing_record.review = review
        db.commit()
        db.refresh(existing_record)
        return existing_record

    # Create new record
    record = BookRecord(
        user_id=current_user.id, book_id=book_id, rating=rating, review=review
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/api/records")
async def get_records(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    # Get the current user's book records
    records = db.query(BookRecord).filter(BookRecord.user_id == current_user.id).all()
    return records
