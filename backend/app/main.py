from fastapi import FastAPI

from .database import Base, engine
from . import models  # noqa: F401 - ensure models are registered with SQLAlchemy metadata

# Create database tables on startup.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="0.2.0")


@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v0.2.0", "status": "running"}


@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "0.2.0", "database": "connected"}
