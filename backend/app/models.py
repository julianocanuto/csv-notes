"""Database models for CSV Notes Manager."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class CSVImport(Base):
    """Model representing a tracked CSV import."""

    __tablename__ = "csv_imports"

    import_id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    import_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    row_count = Column(Integer, nullable=False, default=0)
    primary_key_column = Column(String, nullable=False, default="ID")


class CSVRow(Base):
    """Model representing a single row from an imported CSV file."""

    __tablename__ = "csv_rows"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    primary_key_value = Column(Integer, nullable=False, unique=True, index=True)
    first_import_id = Column(Integer, ForeignKey("csv_imports.import_id"))
    last_seen_import_id = Column(Integer, ForeignKey("csv_imports.import_id"))
    is_orphaned = Column(Boolean, nullable=False, default=False)

    notes = relationship("Note", back_populates="row", cascade="all, delete-orphan")


class Note(Base):
    """Model representing a note attached to a CSV row."""

    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, autoincrement=True)
    row_id = Column(Integer, ForeignKey("csv_rows.row_id"), nullable=False)
    note_text = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="Open")
    created_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_deleted = Column(Boolean, nullable=False, default=False)

    row = relationship("CSVRow", back_populates="notes")
