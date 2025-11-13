from fastapi import FastAPI

from .database import Base, engine
from . import models  # noqa: F401 - ensure models are registered with SQLAlchemy metadata
from .api import csv, notes

# Create database tables on startup.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="1.1.0")

app.include_router(csv.router, prefix="/api/v1/csv", tags=["CSV"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Notes"])


@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v1.1.0", "status": "running"}


@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "1.1.0"}
