"""Database models for CSV Notes Manager."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class CSVImport(Base):
    """Model representing a tracked CSV import."""

    __tablename__ = "csv_imports"

    import_id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    import_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    row_count = Column(Integer, nullable=False, default=0)
    primary_key_column = Column(String, nullable=False, default="ID")
