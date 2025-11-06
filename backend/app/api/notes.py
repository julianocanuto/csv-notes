"""Notes API endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CSVRow, Note

router = APIRouter()


class NoteCreate(BaseModel):
    """Schema for creating a new note."""

    row_id: str = Field(..., min_length=1)
    note_text: str = Field(..., min_length=1)
    status: str = Field(default="Open", min_length=1)


@router.post("/")
async def create_note(note: NoteCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Create a new note for a CSV row."""

    identifier = note.row_id.strip()
    internal_row_id: int | None = None
    try:
        internal_row_id = int(identifier)
    except ValueError:
        internal_row_id = None

    query = db.query(CSVRow)
    row = None
    if internal_row_id is not None:
        row = query.filter(CSVRow.row_id == internal_row_id).first()

    if row is None:
        row = query.filter(CSVRow.primary_key_value == identifier).first()
    if not row:
        # No existing CSV row has been persisted yet. Create a lightweight row so
        # that notes can still be attached to arbitrary identifiers.
        row = CSVRow(
            primary_key_value=identifier,
            first_import_id=None,
            last_seen_import_id=None,
            is_orphaned=True,
        )
        db.add(row)
        db.flush()

    new_note = Note(
        row_id=row.row_id,
        note_text=note.note_text,
        status=note.status,
        created_timestamp=datetime.utcnow(),
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        "success": True,
        "note_id": new_note.note_id,
        "row_id": row.row_id,
        "primary_key_value": row.primary_key_value,
        "note_text": new_note.note_text,
        "status": new_note.status,
        "created_timestamp": new_note.created_timestamp.isoformat(),
    }


@router.get("/")
async def list_notes(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Retrieve all non-deleted notes ordered by newest first."""

    notes = (
        db.query(Note)
        .filter(Note.is_deleted == False)  # noqa: E712
        .order_by(Note.created_timestamp.desc())
        .all()
    )

    return {
        "success": True,
        "notes": [
            {
                "note_id": item.note_id,
                "row_id": item.row_id,
                "primary_key_value": item.row.primary_key_value if item.row else None,
                "note_text": item.note_text,
                "status": item.status,
                "created_timestamp": item.created_timestamp.isoformat(),
            }
            for item in notes
        ],
    }


@router.get("/by-row/{row_id}")
async def get_notes_for_row(row_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Retrieve notes for a specific CSV row."""

    identifier = row_id.strip()
    internal_row_id: int | None = None
    try:
        internal_row_id = int(identifier)
    except ValueError:
        internal_row_id = None

    query = db.query(CSVRow)
    row = None
    if internal_row_id is not None:
        row = query.filter(CSVRow.row_id == internal_row_id).first()

    if row is None:
        row = query.filter(CSVRow.primary_key_value == identifier).first()
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")

    notes = (
        db.query(Note)
        .filter(Note.row_id == row.row_id, Note.is_deleted == False)  # noqa: E712
        .order_by(Note.created_timestamp.desc())
        .all()
    )

    return {
        "success": True,
        "notes": [
            {
                "note_id": item.note_id,
                "row_id": item.row_id,
                "primary_key_value": row.primary_key_value,
                "note_text": item.note_text,
                "status": item.status,
                "created_timestamp": item.created_timestamp.isoformat(),
            }
            for item in notes
        ],
    }

