# Project Structure & Organization

## Root Directory Layout

```
csv-notes-manager/
├── backend/                 # Python FastAPI backend
├── frontend/               # React frontend application  
├── data/                   # SQLite database storage (gitignored)
├── .kiro/                  # Kiro configuration and steering
├── docker-compose.yml      # Production Docker setup
├── docker-compose.dev.yml  # Development Docker setup
├── Dockerfile             # Backend container definition
└── documentation files    # README, CONTRIBUTING, etc.
```

## Backend Structure (`backend/`)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── database.py        # SQLAlchemy setup and session management
│   ├── models.py          # Database models (CSVImport, CSVRow, Note, Tag)
│   └── api/               # API route handlers
│       ├── __init__.py
│       ├── csv.py         # CSV import/export endpoints
│       └── notes.py       # Note CRUD endpoints
└── requirements.txt       # Python dependencies
```

## Frontend Structure (`frontend/`)

```
frontend/
├── src/
│   ├── main.jsx          # React app entry point
│   ├── App.jsx           # Root component with routing
│   └── components/       # React components
│       ├── NotesList.jsx      # Display and manage notes
│       └── CsvImportsViewer.jsx # Browse CSV data with notes
├── package.json          # Node.js dependencies and scripts
├── vite.config.js        # Vite build configuration
└── index.html           # HTML template
```

## Key Files & Responsibilities

### Backend Core Files
- **`main.py`**: FastAPI application setup, router registration, health endpoints
- **`database.py`**: SQLAlchemy engine, session management, database connection
- **`models.py`**: All database models with relationships and constraints
- **`api/csv.py`**: CSV import, metadata tracking, file processing
- **`api/notes.py`**: Note CRUD operations, tag management

### Frontend Core Files  
- **`App.jsx`**: Main application layout, state management, component orchestration
- **`NotesList.jsx`**: Note display, editing, filtering by row ID
- **`CsvImportsViewer.jsx`**: CSV data browser with inline notes column

### Configuration Files
- **`docker-compose.yml`**: Production deployment with built frontend
- **`docker-compose.dev.yml`**: Development setup with hot reload
- **`Dockerfile`**: Backend container with Python 3.10 Alpine
- **`requirements.txt`**: FastAPI, SQLAlchemy, uvicorn dependencies
- **`package.json`**: React, Ant Design, Vite dependencies

## Data Storage

- **Database**: `data/notes.db` (SQLite, persistent across container restarts)
- **Uploads**: Temporary CSV files processed in-memory
- **Logs**: Application logs (when implemented)

## Development Workflow

1. **Feature branches**: All changes start in separate branch from main
2. **Docker-first**: Use docker-compose.dev.yml for consistent environment  
3. **API-first**: Backend endpoints developed before frontend integration
4. **Component-based**: Frontend organized as reusable React components
5. **Database-first**: Models define schema, migrations handled by SQLAlchemy

## Import Patterns

- **Backend**: Relative imports within app package (`from .database import Base`)
- **Frontend**: ES6 imports with explicit file extensions for components
- **API calls**: Frontend uses fetch() with proxy to backend during development