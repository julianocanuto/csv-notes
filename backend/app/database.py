"""Database configuration module for CSV Notes Manager."""
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

# Resolve the database URL from environment variables with a SQLite fallback.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/notes.db")

# Ensure the SQLite data directory exists when using SQLite file storage.
if DATABASE_URL.startswith("sqlite"):
    sqlite_url = make_url(DATABASE_URL)
    db_path = sqlite_url.database
    if db_path and db_path != ":memory:":
        Path(db_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a SQLAlchemy database session and ensure cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
