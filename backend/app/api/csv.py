"""CSV import API endpoints."""
from __future__ import annotations

import csv
import io
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CSVImport, CSVRow

router = APIRouter()


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

    primary_key_column = "ID" if "ID" in reader.fieldnames else reader.fieldnames[0]

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
        if raw_pk is None or raw_pk == "":
            # Skip rows that do not have a primary key value.
            continue

        try:
            pk_value = int(str(raw_pk).strip())
        except ValueError:
            # Skip rows where the primary key cannot be converted to an integer.
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
