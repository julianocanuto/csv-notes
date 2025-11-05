"""CSV import API endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CSVImport

router = APIRouter()


@router.post("/import")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Import a CSV file and record its metadata."""
    contents = await file.read()

    try:
        decoded = contents.decode()
    except UnicodeDecodeError:
        decoded = contents.decode("utf-8", errors="ignore")

    lines = decoded.splitlines()
    row_count = max(len(lines) - 1, 0) if lines else 0

    csv_import = CSVImport(
        filename=file.filename,
        import_timestamp=datetime.utcnow(),
        row_count=row_count,
        primary_key_column="ID",
    )

    db.add(csv_import)
    db.commit()
    db.refresh(csv_import)

    return {
        "success": True,
        "import_id": csv_import.import_id,
        "filename": csv_import.filename,
        "row_count": csv_import.row_count,
        "message": f"CSV uploaded with {row_count} rows",
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
