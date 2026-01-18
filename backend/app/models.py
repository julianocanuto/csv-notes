"""Database models for CSV Notes Manager."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, Table
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

    snapshots = relationship(
        "CSVRowSnapshot",
        back_populates="csv_import",
        cascade="all, delete-orphan",
    )
    schema = relationship(
        "CSVImportSchema",
        back_populates="csv_import",
        cascade="all, delete-orphan",
        uselist=False,
    )


class CSVRow(Base):
    """Model representing a single row from an imported CSV file."""

    __tablename__ = "csv_rows"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    primary_key_value = Column(String, nullable=False, unique=True, index=True)
    first_import_id = Column(Integer, ForeignKey("csv_imports.import_id"))
    last_seen_import_id = Column(Integer, ForeignKey("csv_imports.import_id"))
    is_orphaned = Column(Boolean, nullable=False, default=False)

    notes = relationship("Note", back_populates="row", cascade="all, delete-orphan")
    snapshots = relationship(
        "CSVRowSnapshot",
        back_populates="row",
        cascade="all, delete-orphan",
    )


class CSVImportSchema(Base):
    """Schema metadata for an imported CSV file."""

    __tablename__ = "csv_import_schemas"

    import_id = Column(
        Integer,
        ForeignKey("csv_imports.import_id"),
        primary_key=True,
    )
    columns = Column(JSON, nullable=False)

    csv_import = relationship("CSVImport", back_populates="schema")


class CSVRowSnapshot(Base):
    """Snapshot of row data for a given CSV import."""

    __tablename__ = "csv_row_snapshots"

    snapshot_id = Column(Integer, primary_key=True, autoincrement=True)
    row_id = Column(Integer, ForeignKey("csv_rows.row_id"), nullable=False)
    import_id = Column(Integer, ForeignKey("csv_imports.import_id"), nullable=False)
    data = Column(JSON, nullable=False)

    row = relationship("CSVRow", back_populates="snapshots")
    csv_import = relationship("CSVImport", back_populates="snapshots")


note_tags_association = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.note_id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.tag_id"), primary_key=True),
)


class Tag(Base):
    """Tag assigned to notes for categorization."""

    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    created_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    notes = relationship(
        "Note",
        secondary=note_tags_association,
        back_populates="tags",
    )


class Note(Base):
    """Model representing a note attached to a CSV row."""

    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, autoincrement=True)
    row_id = Column(Integer, ForeignKey("csv_rows.row_id"), nullable=False)
    note_text = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="Open")
    created_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_timestamp = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    row = relationship("CSVRow", back_populates="notes")
    tags = relationship(
        "Tag",
        secondary=note_tags_association,
        back_populates="notes",
        lazy="joined",
    )
