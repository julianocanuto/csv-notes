from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="CSV Notes Manager", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v0.1.0", "status": "running"}


@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "0.1.0"}
