import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./booktracker.db")

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "this-is-a-random-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
