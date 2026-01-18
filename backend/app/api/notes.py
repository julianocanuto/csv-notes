"""Notes API endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import CSVRow, Note, Tag

router = APIRouter()


STATUS_CHOICES = {"Open", "In Progress", "Resolved", "Closed"}


def _normalize_status(status: str | None) -> str:
    if not status:
        return "Open"
    normalized = status.strip()
    if not normalized:
        return "Open"
    title_cased = normalized.title()
    if title_cased not in STATUS_CHOICES:
        raise HTTPException(status_code=400, detail="Invalid status provided")
    return title_cased


def _normalize_tags(tags: Iterable[str]) -> List[str]:
    cleaned: List[str] = []
    seen = set()
    for tag in tags:
        value = tag.strip()
        if not value:
            continue
        normalized = value.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        cleaned.append(value)
    return cleaned


class NoteCreate(BaseModel):
    """Schema for creating a new note."""

    row_id: str = Field(..., min_length=1)
    note_text: str = Field(..., min_length=1)
    status: str = Field(default="Open", min_length=1)
    tags: List[str] = Field(default_factory=list)


class NoteUpdate(BaseModel):
    """Schema for updating a note."""

    note_text: str | None = Field(default=None, min_length=1)
    status: str | None = Field(default=None, min_length=1)
    tags: List[str] | None = None


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
        status=_normalize_status(note.status),
        created_timestamp=datetime.utcnow(),
    )

    db.add(new_note)
    db.flush()

    tags_to_assign = _normalize_tags(note.tags)
    if tags_to_assign:
        for tag_name in tags_to_assign:
            normalized = tag_name.lower()
            existing_tag = (
                db.query(Tag)
                .filter(func.lower(Tag.name) == normalized)
                .one_or_none()
            )
            if not existing_tag:
                existing_tag = Tag(name=tag_name)
                db.add(existing_tag)
                db.flush()
            new_note.tags.append(existing_tag)

    db.commit()
    db.refresh(new_note)

    return {
        "success": True,
        "note_id": new_note.note_id,
        "row_id": row.row_id,
        "primary_key_value": row.primary_key_value,
        "note_text": new_note.note_text,
        "status": new_note.status,
        "tags": [tag.name for tag in new_note.tags],
        "created_timestamp": new_note.created_timestamp.isoformat(),
        "updated_timestamp": new_note.updated_timestamp.isoformat(),
    }


@router.get("/")
async def list_notes(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Retrieve all non-deleted notes ordered by newest first."""

    notes = (
        db.query(Note)
        .options(joinedload(Note.tags))
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
                "tags": [tag.name for tag in item.tags],
                "created_timestamp": item.created_timestamp.isoformat(),
                "updated_timestamp": item.updated_timestamp.isoformat(),
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
        .options(joinedload(Note.tags))
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
                "tags": [tag.name for tag in item.tags],
                "created_timestamp": item.created_timestamp.isoformat(),
                "updated_timestamp": item.updated_timestamp.isoformat(),
            }
            for item in notes
        ],
    }


@router.patch("/{note_id}")
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Update mutable fields on a note."""

    note = (
        db.query(Note)
        .options(joinedload(Note.tags), joinedload(Note.row))
        .filter(Note.note_id == note_id, Note.is_deleted == False)  # noqa: E712
        .one_or_none()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    updated = False

    if payload.note_text is not None:
        note.note_text = payload.note_text
        updated = True

    if payload.status is not None:
        note.status = _normalize_status(payload.status)
        updated = True

    if payload.tags is not None:
        updated = True
        note.tags.clear()
        tags_to_assign = _normalize_tags(payload.tags)
        for tag_name in tags_to_assign:
            normalized = tag_name.lower()
            existing_tag = (
                db.query(Tag)
                .filter(func.lower(Tag.name) == normalized)
                .one_or_none()
            )
            if not existing_tag:
                existing_tag = Tag(name=tag_name)
                db.add(existing_tag)
                db.flush()
            note.tags.append(existing_tag)

    if not updated:
        return {
            "success": True,
            "note_id": note.note_id,
            "row_id": note.row_id,
            "primary_key_value": note.row.primary_key_value if note.row else None,
            "note_text": note.note_text,
            "status": note.status,
            "tags": [tag.name for tag in note.tags],
            "created_timestamp": note.created_timestamp.isoformat(),
            "updated_timestamp": note.updated_timestamp.isoformat(),
        }

    note.updated_timestamp = datetime.utcnow()
    db.add(note)
    db.commit()
    db.refresh(note)

    return {
        "success": True,
        "note_id": note.note_id,
        "row_id": note.row_id,
        "primary_key_value": note.row.primary_key_value if note.row else None,
        "note_text": note.note_text,
        "status": note.status,
        "tags": [tag.name for tag in note.tags],
        "created_timestamp": note.created_timestamp.isoformat(),
        "updated_timestamp": note.updated_timestamp.isoformat(),
    }

