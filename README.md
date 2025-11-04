# CSV Notes Manager

Version: 0.1.0

## Quick Start

### Using Docker (Recommended)
```bash
docker-compose up -d
```

Visit: http://localhost:8080

### Manual Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## API Endpoints
- GET / - Welcome message
- GET /api/v1/health - Health check

### Testing
```bash
# Build and run
docker-compose up -d

# Test
curl http://localhost:8080/
curl http://localhost:8080/api/v1/health

# Expected responses:
# {"message": "CSV Notes Manager v0.1.0", "status": "running"}
# {"status": "healthy", "version": "0.1.0"}
```
