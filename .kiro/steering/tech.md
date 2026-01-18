# Technology Stack & Build System

## Backend Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI 0.104+ (async, auto-documentation, type hints)
- **Database**: SQLite 3 with SQLAlchemy 2.0+ ORM
- **File Processing**: python-multipart for CSV uploads
- **Server**: Uvicorn ASGI server

## Frontend Stack

- **Framework**: React 18 with functional components and hooks
- **UI Library**: Ant Design 5.x (enterprise-grade tables and components)
- **Build Tool**: Vite 5.x (fast HMR, optimized builds)
- **Package Manager**: npm

## Database Architecture

- **SQLite**: Local database stored in `data/notes.db`
- **Models**: CSVImport, CSVRow, Note, Tag with proper relationships
- **Schema**: Supports orphaned row tracking, note versioning, and tag associations
- **Migrations**: Handled by SQLAlchemy metadata.create_all()

## Development Commands

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev  # Starts on port 3000 with proxy to backend
```

### Docker Development (Recommended)
```bash
# Full development environment with hot reload
docker-compose -f docker-compose.dev.yml up

# Production build
docker-compose up --build
```

### Testing
```bash
# Backend tests (when implemented)
cd backend && pytest

# Frontend tests (when implemented)  
cd frontend && npm test
```

## Build & Deployment

- **Development**: docker-compose.dev.yml with hot reload
- **Production**: docker-compose.yml with built frontend served by backend
- **Database**: Persistent volume mounted to `./data` directory
- **Ports**: Backend on 8080, Frontend on 3000 (dev) or 80 (prod)

## API Structure

- **Base URL**: `/api/v1/`
- **CSV Endpoints**: `/api/v1/csv/` (import, list imports)
- **Notes Endpoints**: `/api/v1/notes/` (CRUD operations)
- **Documentation**: Available at `/docs` (Swagger UI)

## Code Style

- **Python**: Black formatter, type hints required
- **JavaScript**: Functional components, hooks pattern
- **Commits**: Conventional Commits format required
- **Branching**: Feature branches, PR required for main