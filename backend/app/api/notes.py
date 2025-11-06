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

    row_id: int
    note_text: str = Field(..., min_length=1)
    status: str = Field(default="Open", min_length=1)


@router.post("/")
async def create_note(note: NoteCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Create a new note for a CSV row."""

    row = db.query(CSVRow).filter(CSVRow.row_id == note.row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")

    new_note = Note(
        row_id=note.row_id,
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
        "note_text": new_note.note_text,
        "status": new_note.status,
        "created_timestamp": new_note.created_timestamp.isoformat(),
    }


@router.get("/by-row/{row_id}")
async def get_notes_for_row(row_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Retrieve notes for a specific CSV row."""

    notes = (
        db.query(Note)
        .filter(Note.row_id == row_id, Note.is_deleted == False)  # noqa: E712
        .order_by(Note.created_timestamp.desc())
        .all()
    )

    return {
        "success": True,
        "notes": [
            {
                "note_id": item.note_id,
                "note_text": item.note_text,
                "status": item.status,
                "created_timestamp": item.created_timestamp.isoformat(),
            }
            for item in notes
        ],
    }

