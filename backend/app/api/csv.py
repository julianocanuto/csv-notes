"""CSV import API endpoints."""
from __future__ import annotations

import csv
import io
from collections import Counter
from datetime import datetime
from typing import Any, Dict, Iterable, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CSVImport, CSVRow

router = APIRouter()


PRIMARY_KEY_HINTS = {
    "id": 5,
    "row_id": 4,
    "primary_key": 4,
    "primarykey": 4,
    "pk": 3,
    "record_id": 3,
    "uuid": 3,
    "key": 2,
}


def _score_column(name: str, rows: Iterable[Dict[str, Any]], total_rows: int) -> float:
    """Score a column for primary key suitability."""

    normalized = name.strip()
    if not normalized:
        return float("-inf")

    lowered = normalized.lower()
    score = PRIMARY_KEY_HINTS.get(lowered, 0)

    values: List[str] = []
    unique_values = set()
    duplicates = False

    for row in rows:
        raw_value = row.get(name)
        if raw_value is None:
            continue
        value = str(raw_value).strip()
        if not value:
            continue
        values.append(value)
        if value in unique_values:
            duplicates = True
        unique_values.add(value)

    non_empty = len(values)

    if total_rows and non_empty:
        coverage = non_empty / total_rows
        score += coverage * 3
    elif non_empty:
        score += 1

    if not duplicates and non_empty:
        score += 5
    else:
        duplicate_count = Counter(values)
        penalty = sum(count - 1 for count in duplicate_count.values())
        score -= min(penalty, 5)

    # Prefer columns with longer value length variety as a minor heuristic.
    if unique_values:
        average_length = sum(len(value) for value in unique_values) / len(unique_values)
        score += min(average_length / 10, 2)

    return score


def detect_primary_key_column(fieldnames: List[str], rows: List[Dict[str, Any]]) -> str:
    """Determine the most likely primary key column from a CSV file."""

    if not fieldnames:
        raise HTTPException(status_code=400, detail="CSV file is missing a header row")

    if not rows:
        for candidate in ("id", "row_id", "pk", "primary_key"):
            for field in fieldnames:
                if field.strip().lower() == candidate:
                    return field
        return fieldnames[0]

    total_rows = len(rows)
    best_column = fieldnames[0]
    best_score = float("-inf")

    for index, name in enumerate(fieldnames):
        score = _score_column(name, rows, total_rows)
        # Small bonus for earlier columns to break ties deterministically.
        score -= index * 0.1
        if score > best_score:
            best_score = score
            best_column = name

    return best_column


@router.post("/import")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Import a CSV file, track its metadata, and persist row references."""
    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        decoded = contents.decode()
    except UnicodeDecodeError:
        decoded = contents.decode("utf-8", errors="ignore")

    csv_buffer = io.StringIO(decoded)
    reader = csv.DictReader(csv_buffer)

    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV file is missing a header row")

    rows = list(reader)
    row_count = len(rows)

    primary_key_column = detect_primary_key_column(reader.fieldnames, rows)

    csv_import = CSVImport(
        filename=file.filename,
        import_timestamp=datetime.utcnow(),
        row_count=row_count,
        primary_key_column=primary_key_column,
    )

    db.add(csv_import)
    db.flush()

    for record in rows:
        raw_pk = record.get(primary_key_column)
        if raw_pk is None:
            # Skip rows that do not have a primary key value.
            continue

        pk_value = str(raw_pk).strip()
        if pk_value == "":
            # Skip rows that normalize to an empty value.
            continue

        existing_row = (
            db.query(CSVRow)
            .filter(CSVRow.primary_key_value == pk_value)
            .one_or_none()
        )

        if existing_row:
            existing_row.last_seen_import_id = csv_import.import_id
            existing_row.is_orphaned = False
            continue

        csv_row = CSVRow(
            primary_key_value=pk_value,
            first_import_id=csv_import.import_id,
            last_seen_import_id=csv_import.import_id,
            is_orphaned=False,
        )
        db.add(csv_row)

    db.commit()
    db.refresh(csv_import)

    return {
        "success": True,
        "import_id": csv_import.import_id,
        "filename": csv_import.filename,
        "row_count": csv_import.row_count,
        "primary_key": primary_key_column,
    }


@router.get("/imports")
async def list_imports(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """List previously imported CSV files."""
    imports = db.query(CSVImport).order_by(CSVImport.import_timestamp.desc()).all()
    return {
        "success": True,
        "imports": [
            {
                "import_id": item.import_id,
                "filename": item.filename,
                "row_count": item.row_count,
                "timestamp": item.import_timestamp.isoformat(),
            }
            for item in imports
        ],
    }
