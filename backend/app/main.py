from fastapi import FastAPI

from .database import Base, engine
from . import models  # noqa: F401 - ensure models are registered with SQLAlchemy metadata
from .api import csv

# Create database tables on startup.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="0.3.0")

app.include_router(csv.router, prefix="/api/v1/csv", tags=["CSV"])


@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v0.3.0", "status": "running"}


@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "0.3.0", "database": "connected"}
