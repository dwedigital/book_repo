from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# User Schemas
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# BookRecord Schemas
class BookRecordBase(BaseModel):
    book_id: int
    rating: Optional[float] = None
    review: Optional[str] = None
    date_read: Optional[datetime] = None


class BookRecordCreate(BookRecordBase):
    pass


class BookRecord(BookRecordBase):
    id: int
    user_id: int
    created_at: datetime
    book: Book

    class Config:
        orm_mode = True
