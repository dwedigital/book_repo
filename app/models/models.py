from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Add this field

    books = relationship("BookRecord", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)

    records = relationship("BookRecord", back_populates="book")


class BookRecord(Base):
    __tablename__ = "book_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    rating = Column(Float, nullable=True)
    review = Column(Text, nullable=True)
    date_read = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="books")
    book = relationship("Book", back_populates="records")
