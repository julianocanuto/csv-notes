# CSV Notes Manager - Incremental Development Plan

**Version:** 1.0  
**Last Updated:** 2025-11-04  
**Status:** Ready for Implementation

---

## Overview

This development plan breaks down the CSV Notes Manager into **small, self-contained steps** where each step produces a **working, deployable, testable version** of the application. Every increment includes Docker deployment from the very first working version (v0.1.0).

### Core Principles

✅ **Small Steps**: Each task is focused and minimal (1-3 hours max)  
✅ **Always Working**: Every version is deployable and testable  
✅ **Incremental**: Build layer by layer, starting with MVP  
✅ **Easy to Review**: Changes small enough for 5-10 minute review  
✅ **Docker First**: Container deployment from v0.1.0 onwards

---

## Table of Contents

1. [Version 0.1.0 - Hello World + Docker](#version-010---hello-world--docker)
2. [Version 0.2.0 - Database Foundation](#version-020---database-foundation)
3. [Version 0.3.0 - Basic CSV Import](#version-030---basic-csv-import)
4. [Version 0.4.0 - Simple Data Display](#version-040---simple-data-display)
5. [Version 0.5.0 - Single Note Creation](#version-050---single-note-creation)
6. [Version 0.6.0 - Note Display](#version-060---note-display)
7. [Version 0.7.0 - Note Editing](#version-070---note-editing)
8. [Version 0.8.0 - Note Tags](#version-080---note-tags)
9. [Version 0.9.0 - Primary Key Detection](#version-090---primary-key-detection)
10. [Version 1.0.0 - MVP Complete](#version-100---mvp-complete)
11. [Version 1.1.0 - Orphaned Rows](#version-110---orphaned-rows)
12. [Version 1.2.0 - Basic Filters](#version-120---basic-filters)
13. [Version 1.3.0 - Custom Views](#version-130---custom-views)
14. [Version 1.4.0 - Export Functionality](#version-140---export-functionality)
15. [Version 1.5.0 - Production Ready](#version-150---production-ready)

---

## Version 0.1.0 - Hello World + Docker

**Goal**: Create minimal working app with Docker deployment

**Duration**: 2-3 hours  
**Review Time**: 5 minutes

### Tasks

#### Task 0.1.1: Project Structure Setup
**Files to Create**:
```
csv-notes-manager/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
├── .gitignore
├── README.md
├── Dockerfile
└── docker-compose.yml
```

**Implementation**:

**`backend/requirements.txt`**:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

**`backend/app/main.py`**:
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="CSV Notes Manager", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v0.1.0", "status": "running"}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "0.1.0"}
```

**`Dockerfile`**:
```dockerfile
FROM python:3.10-alpine

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**`docker-compose.yml`**:
```yaml
version: '3.8'

services:
  csv-notes:
    build: .
    container_name: csv-notes-manager
    ports:
      - "8080:8080"
    restart: unless-stopped
```

**`README.md`**:
```markdown
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
```

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

### ✅ Definition of Done
- [ ] Docker container builds successfully
- [ ] Application starts on port 8080
- [ ] Health check endpoint responds
- [ ] README has deployment instructions
- [ ] Can be stopped and restarted without errors

---

## Version 0.2.0 - Database Foundation

**Goal**: Add SQLite database with single table

**Duration**: 2-3 hours  
**Review Time**: 8 minutes

### Tasks

#### Task 0.2.1: Add Database Dependencies
**Files to Modify**: `backend/requirements.txt`
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
```

#### Task 0.2.2: Create Database Configuration
**Files to Create**: `backend/app/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/notes.db")

# Create data directory if it doesn't exist
os.makedirs("./data", exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Task 0.2.3: Create First Model
**Files to Create**: `backend/app/models.py`
```python
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class CSVImport(Base):
    __tablename__ = "csv_imports"
    
    import_id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    import_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    row_count = Column(Integer, nullable=False, default=0)
    primary_key_column = Column(String, nullable=False, default="ID")
```

#### Task 0.2.4: Update Main App
**Files to Modify**: `backend/app/main.py`
```python
from fastapi import FastAPI
from .database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="0.2.0")

@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v0.2.0", "status": "running"}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "0.2.0", "database": "connected"}
```

#### Task 0.2.5: Update Docker Configuration
**Files to Modify**: `docker-compose.yml`
```yaml
version: '3.8'

services:
  csv-notes:
    build: .
    container_name: csv-notes-manager
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///./data/notes.db
    restart: unless-stopped
```

### Testing
```bash
# Rebuild and run
docker-compose down
docker-compose up --build -d

# Test
curl http://localhost:8080/api/v1/health

# Verify database created
ls -la data/
# Should see: notes.db

# Check with SQLite
sqlite3 data/notes.db "SELECT name FROM sqlite_master WHERE type='table';"
# Should see: csv_imports
```

### ✅ Definition of Done
- [ ] SQLite database created in data/ directory
- [ ] csv_imports table exists
- [ ] Database persists across container restarts
- [ ] Health check confirms database connection
- [ ] Can query database manually

---

## Version 0.3.0 - Basic CSV Import

**Goal**: Upload CSV and store metadata (no data processing yet)

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Tasks

#### Task 0.3.1: Add File Upload Dependencies
**Files to Modify**: `backend/requirements.txt`
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-multipart==0.0.6
```

#### Task 0.3.2: Create CSV Upload Endpoint
**Files to Create**: `backend/app/api/__init__.py` (empty)

**Files to Create**: `backend/app/api/csv.py`
```python
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CSVImport
from datetime import datetime

router = APIRouter()

@router.post("/import")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file temporarily
    contents = await file.read()
    
    # Count lines (simple row count)
    row_count = len(contents.decode().splitlines()) - 1  # -1 for header
    
    # Create import record
    csv_import = CSVImport(
        filename=file.filename,
        import_timestamp=datetime.utcnow(),
        row_count=row_count,
        primary_key_column="ID"
    )
    
    db.add(csv_import)
    db.commit()
    db.refresh(csv_import)
    
    return {
        "success": True,
        "import_id": csv_import.import_id,
        "filename": csv_import.filename,
        "row_count": csv_import.row_count,
        "message": f"CSV uploaded with {row_count} rows"
    }

@router.get("/imports")
async def list_imports(db: Session = Depends(get_db)):
    imports = db.query(CSVImport).order_by(CSVImport.import_timestamp.desc()).all()
    return {
        "success": True,
        "imports": [
            {
                "import_id": i.import_id,
                "filename": i.filename,
                "row_count": i.row_count,
                "timestamp": i.import_timestamp.isoformat()
            }
            for i in imports
        ]
    }
```

#### Task 0.3.3: Wire Up API Router
**Files to Modify**: `backend/app/main.py`
```python
from fastapi import FastAPI
from .database import engine, Base
from .api import csv

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="0.3.0")

app.include_router(csv.router, prefix="/api/v1/csv", tags=["CSV"])

@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v0.3.0", "status": "running"}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "0.3.0", "database": "connected"}
```

### Testing
```bash
# Rebuild
docker-compose down
docker-compose up --build -d

# Create test CSV
echo -e "ID,Name,Value\n1,Test,100\n2,Test2,200" > test.csv

# Upload CSV
curl -X POST -F "file=@test.csv" http://localhost:8080/api/v1/csv/import

# View imports
curl http://localhost:8080/api/v1/csv/imports
```

### ✅ Definition of Done
- [ ] Can upload CSV file via API
- [ ] Import metadata saved to database
- [ ] Can list all imports
- [ ] File upload works via curl
- [ ] Swagger docs show endpoint (http://localhost:8080/docs)

---

## Version 0.4.0 - Simple Data Display

**Goal**: Add basic React frontend that shows "Hello World"

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Tasks

#### Task 0.4.1: Create Frontend Structure
**Files to Create**:
```
frontend/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.jsx
│   └── App.jsx
```

**`frontend/package.json`**:
```json
{
  "name": "csv-notes-frontend",
  "version": "0.4.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

**`frontend/vite.config.js`**:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
})
```

**`frontend/index.html`**:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CSV Notes Manager</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

**`frontend/src/main.jsx`**:
```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

**`frontend/src/App.jsx`**:
```javascript
import React, { useState, useEffect } from 'react'

function App() {
  const [health, setHealth] = useState(null)

  useEffect(() => {
    fetch('/api/v1/health')
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(err => console.error(err))
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>CSV Notes Manager v0.4.0</h1>
      {health && (
        <div>
          <p>Status: {health.status}</p>
          <p>Version: {health.version}</p>
          <p>Database: {health.database}</p>
        </div>
      )}
    </div>
  )
}

export default App
```

#### Task 0.4.2: Update Docker for Development
**Files to Create**: `docker-compose.dev.yml`
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./backend/app:/app/app
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///./data/notes.db
    restart: unless-stopped

  frontend:
    image: node:18-alpine
    working_dir: /app
    command: sh -c "npm install && npm run dev -- --host"
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    environment:
      - CHOKIDAR_USEPOLLING=true
```

### Testing
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up

# Frontend: http://localhost:3000
# Backend: http://localhost:8080
# Should see health status on page
```

### ✅ Definition of Done
- [ ] React app runs and connects to backend
- [ ] Health status displayed on page
- [ ] Development environment with hot reload
- [ ] Frontend can call backend API
- [ ] Browser shows v0.4.0

---

## Version 0.5.0 - Single Note Creation

**Goal**: Add minimal note creation (no tags, just text)

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Tasks

#### Task 0.5.1: Add Note Models
**Files to Modify**: `backend/app/models.py`
```python
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class CSVImport(Base):
    __tablename__ = "csv_imports"
    
    import_id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    import_timestamp = Column(DateTime, default=datetime.utcnow)
    row_count = Column(Integer, default=0)
    primary_key_column = Column(String, default="ID")

class CSVRow(Base):
    __tablename__ = "csv_rows"
    
    row_id = Column(Integer, primary_key=True)
    primary_key_value = Column(Integer, nullable=False, unique=True, index=True)
    first_import_id = Column(Integer, ForeignKey('csv_imports.import_id'))
    last_seen_import_id = Column(Integer, ForeignKey('csv_imports.import_id'))
    is_orphaned = Column(Boolean, default=False)
    
    notes = relationship("Note", back_populates="row")

class Note(Base):
    __tablename__ = "notes"
    
    note_id = Column(Integer, primary_key=True)
    row_id = Column(Integer, ForeignKey('csv_rows.row_id'), nullable=False)
    note_text = Column(Text, nullable=False)
    status = Column(String, default="Open")
    created_timestamp = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    
    row = relationship("CSVRow", back_populates="notes")
```

#### Task 0.5.2: Create Notes API
**Files to Create**: `backend/app/api/notes.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import Note, CSVRow
from datetime import datetime

router = APIRouter()

class NoteCreate(BaseModel):
    row_id: int
    note_text: str
    status: str = "Open"

@router.post("/")
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    # Verify row exists
    row = db.query(CSVRow).filter(CSVRow.row_id == note.row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    
    new_note = Note(
        row_id=note.row_id,
        note_text=note.note_text,
        status=note.status,
        created_timestamp=datetime.utcnow()
    )
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    return {
        "success": True,
        "note_id": new_note.note_id,
        "note_text": new_note.note_text,
        "status": new_note.status,
        "created_timestamp": new_note.created_timestamp.isoformat()
    }

@router.get("/by-row/{row_id}")
async def get_notes_for_row(row_id: int, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(
        Note.row_id == row_id,
        Note.is_deleted == False
    ).order_by(Note.created_timestamp.desc()).all()
    
    return {
        "success": True,
        "notes": [
            {
                "note_id": n.note_id,
                "note_text": n.note_text,
                "status": n.status,
                "created_timestamp": n.created_timestamp.isoformat()
            }
            for n in notes
        ]
    }
```

#### Task 0.5.3: Wire Up Notes Router
**Files to Modify**: `backend/app/main.py`
```python
from fastapi import FastAPI
from .database import engine, Base
from .api import csv, notes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="0.5.0")

app.include_router(csv.router, prefix="/api/v1/csv", tags=["CSV"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Notes"])

@app.get("/")
async def root():
    return {"message": "CSV Notes Manager v0.5.0"}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "0.5.0"}
```

### Testing
```bash
# Rebuild
docker-compose down
docker-compose up --build -d

# First create a test row (manual SQL for now)
sqlite3 data/notes.db "INSERT INTO csv_rows (primary_key_value, first_import_id, last_seen_import_id) VALUES (1, 1, 1);"

# Create note
curl -X POST http://localhost:8080/api/v1/notes/ \
  -H "Content-Type: application/json" \
  -d '{"row_id": 1, "note_text": "Test note", "status": "Open"}'

# Get notes for row
curl http://localhost:8080/api/v1/notes/by-row/1
```

### ✅ Definition of Done
- [ ] Can create note via API
- [ ] Can retrieve notes for a row
- [ ] Notes saved to database
- [ ] Timestamps generated automatically
- [ ] Swagger docs updated

---

## Version 0.6.0 - Note Display

**Goal**: Show notes in frontend (read-only)

**Duration**: 2-3 hours  
**Review Time**: 8 minutes

### Tasks

#### Task 0.6.1: Add Ant Design
**Files to Modify**: `frontend/package.json`
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "antd": "^5.11.0"
  }
}
```

#### Task 0.6.2: Create Simple Note Display
**Files to Create**: `frontend/src/components/NotesList.jsx`
```javascript
import React, { useState, useEffect } from 'react'
import { Card, Tag, Empty } from 'antd'

function NotesList({ rowId }) {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!rowId) return
    
    fetch(`/api/v1/notes/by-row/${rowId}`)
      .then(res => res.json())
      .then(data => {
        setNotes(data.notes || [])
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [rowId])

  if (loading) return <div>Loading...</div>

  if (notes.length === 0) {
    return <Empty description="No notes yet" />
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Notes for Row {rowId}</h3>
      {notes.map(note => (
        <Card key={note.note_id} style={{ marginBottom: '10px' }}>
          <Tag color="blue">{note.status}</Tag>
          <div style={{ marginTop: '8px' }}>{note.note_text}</div>
          <div style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
            {new Date(note.created_timestamp).toLocaleString()}
          </div>
        </Card>
      ))}
    </div>
  )
}

export default NotesList
```

#### Task 0.6.3: Update App to Show Notes
**Files to Modify**: `frontend/src/App.jsx`
```javascript
import React, { useState } from 'react'
import { Button, Input } from 'antd'
import NotesList from './components/NotesList'

function App() {
  const [rowId, setRowId] = useState(1)
  const [inputValue, setInputValue] = useState('1')

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>CSV Notes Manager v0.6.0</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <Input 
          style={{ width: '200px', marginRight: '10px' }}
          placeholder="Enter Row ID"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
        />
        <Button type="primary" onClick={() => setRowId(Number(inputValue))}>
          Load Notes
        </Button>
      </div>
      
      <NotesList rowId={rowId} />
    </div>
  )
}

export default App
```

### Testing
```bash
# Start dev environment
docker-compose -f docker-compose.dev.yml up

# Create test data
sqlite3 data/notes.db <<EOF
INSERT INTO csv_rows (primary_key_value, first_import_id, last_seen_import_id) VALUES (1, 1, 1);
INSERT INTO notes (row_id, note_text, status) VALUES (1, 'First test note', 'Open');
INSERT INTO notes (row_id, note_text, status) VALUES (1, 'Second test note', 'In Progress');
EOF

# Visit http://localhost:3000
# Should see notes displayed
```

### ✅ Definition of Done
- [ ] Notes displayed in frontend
- [ ] Status shown as colored tag
- [ ] Timestamp formatted nicely
- [ ] Can switch between different row IDs
- [ ] Empty state shown when no notes

---

## Version 0.7.0 - Note Editing

**Goal**: Add ability to edit note text and status

**Duration**: 2-3 hours  
**Review Time**: 8 minutes

### Tasks

#### Task 0.7.1: Add Update Endpoint
**Files to Modify**: `backend/app/api/notes.py`
```python
class NoteUpdate(BaseModel):
    note_text: str
    status: str

@router.put("/{note_id}")
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.note_text = note_update.note_text
    note.status = note_update.status
    
    db.commit()
    db.refresh(note)
    
    return {
        "success": True,
        "note_id": note.note_id,
        "note_text": note.note_text,
        "status": note.status
    }
```

#### Task 0.7.2: Add Edit UI
**Files to Create**: `frontend/src/components/NoteEditor.jsx`
```javascript
import React, { useState } from 'react'
import { Modal, Input, Select, Button, message } from 'antd'

const { TextArea } = Input

function NoteEditor({ note, visible, onClose, onSave }) {
  const [text, setText] = useState(note?.note_text || '')
  const [status, setStatus] = useState(note?.status || 'Open')
  const [saving, setSaving] = useState(false)

  const handleSave = async () => {
    setSaving(true)
    try {
      const response = await fetch(`/api/v1/notes/${note.note_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ note_text: text, status })
      })
      
      if (response.ok) {
        message.success('Note updated')
        onSave()
      }
    } catch (err) {
      message.error('Failed to update note')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal
      title="Edit Note"
      open={visible}
      onCancel={onClose}
      footer={[
        <Button key="cancel" onClick={onClose}>Cancel</Button>,
        <Button key="save" type="primary" loading={saving} onClick={handleSave}>
          Save
        </Button>
      ]}
    >
      <div style={{ marginBottom: '16px' }}>
        <label>Status:</label>
        <Select 
          value={status} 
          onChange={setStatus}
          style={{ width: '100%', marginTop: '8px' }}
        >
          <Select.Option value="Open">Open</Select.Option>
          <Select.Option value="In Progress">In Progress</Select.Option>
          <Select.Option value="Resolved">Resolved</Select.Option>
          <Select.Option value="Closed">Closed</Select.Option>
        </Select>
      </div>
      
      <div>
        <label>Note Text:</label>
        <TextArea 
          value={text}
          onChange={e => setText(e.target.value)}
          rows={4}
          style={{ marginTop: '8px' }}
        />
      </div>
    </Modal>
  )
}

export default NoteEditor
```

#### Task 0.7.3: Add Edit Button to Notes List
**Files to Modify**: `frontend/src/components/NotesList.jsx`
```javascript
import React, { useState, useEffect } from 'react'
import { Card, Tag, Empty, Button } from 'antd'
import { EditOutlined } from '@ant-design/icons'
import NoteEditor from './NoteEditor'

function NotesList({ rowId }) {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [editingNote, setEditingNote] = useState(null)

  const loadNotes = () => {
    if (!rowId) return
    
    fetch(`/api/v1/notes/by-row/${rowId}`)
      .then(res => res.json())
      .then(data => {
        setNotes(data.notes || [])
        setLoading(false)
      })
  }

  useEffect(() => {
    loadNotes()
  }, [rowId])

  const handleSave = () => {
    setEditingNote(null)
    loadNotes()
  }

  if (loading) return <div>Loading...</div>
  if (notes.length === 0) return <Empty description="No notes yet" />

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Notes for Row {rowId}</h3>
      {notes.map(note => (
        <Card 
          key={note.note_id} 
          style={{ marginBottom: '10px' }}
          extra={
            <Button 
              icon={<EditOutlined />} 
              onClick={() => setEditingNote(note)}
            >
              Edit
            </Button>
          }
        >
          <Tag color="blue">{note.status}</Tag>
          <div style={{ marginTop: '8px' }}>{note.note_text}</div>
          <div style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
            {new Date(note.created_timestamp).toLocaleString()}
          </div>
        </Card>
      ))}
      
      {editingNote && (
        <NoteEditor
          note={editingNote}
          visible={!!editingNote}
          onClose={() => setEditingNote(null)}
          onSave={handleSave}
        />
      )}
    </div>
  )
}

export default NotesList
```

### Testing
```bash
# Visit http://localhost:3000
# Click "Edit" on a note
# Change text and status
# Save and verify changes persist
```

### ✅ Definition of Done
- [ ] Can click Edit button on notes
- [ ] Modal opens with current note data
- [ ] Can change note text and status
- [ ] Changes saved to database
- [ ] List refreshes after save

---

## Version 0.8.0 - Note Tags

**Goal**: Add tags to notes (create, display, edit)

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Tasks

#### Task 0.8.1: Add Tag Model
**Files to Modify**: `backend/app/models.py`
```python
# Add to Note class:
tags = relationship("NoteTag", back_populates="note", cascade="all, delete-orphan")

# Add new model:
class NoteTag(Base):
    __tablename__ = "note_tags"
    
    tag_id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey('notes.note_id'), nullable=False)
    tag_name = Column(String, nullable=False, index=True)
    
    note = relationship("Note", back_populates="tags")
```

#### Task 0.8.2: Update Notes API for Tags
**Files to Modify**: `backend/app/api/notes.py`
```python
from ..models import Note, CSVRow, NoteTag

class NoteCreate(BaseModel):
    row_id: int
    note_text: str
    status: str = "Open"
    tags: list[str] = []

class NoteUpdate(BaseModel):
    note_text: str
    status: str
    tags: list[str] = []

# Modify create_note to handle tags
@router.post("/")
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    row = db.query(CSVRow).filter(CSVRow.row_id == note.row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    
    new_note = Note(
        row_id=note.row_id,
        note_text=note.note_text,
        status=note.status
    )
    
    db.add(new_note)
    db.flush()  # Get note_id without committing
    
    # Add tags
    for tag_name in note.tags:
        if tag_name.strip():
            tag = NoteTag(note_id=new_note.note_id, tag_name=tag_name.strip())
            db.add(tag)
    
    db.commit()
    db.refresh(new_note)
    
    return {
        "success": True,
        "note_id": new_note.note_id,
        "note_text": new_note.note_text,
        "status": new_note.status,
        "tags": note.tags
    }

# Modify get_notes_for_row to include tags
@router.get("/by-row/{row_id}")
async def get_notes_for_row(row_id: int, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(
        Note.row_id == row_id,
        Note.is_deleted == False
    ).order_by(Note.created_timestamp.desc()).all()
    
    return {
        "success": True,
        "notes": [
            {
                "note_id": n.note_id,
                "note_text": n.note_text,
                "status": n.status,
                "created_timestamp": n.created_timestamp.isoformat(),
                "tags": [t.tag_name for t in n.tags]
            }
            for n in notes
        ]
    }

# Modify update_note to handle tags
@router.put("/{note_id}")
async def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.note_text = note_update.note_text
    note.status = note_update.status
    
    # Update tags: delete old, add new
    db.query(NoteTag).filter(NoteTag.note_id == note_id).delete()
    for tag_name in note_update.tags:
        if tag_name.strip():
            tag = NoteTag(note_id=note_id, tag_name=tag_name.strip())
            db.add(tag)
    
    db.commit()
    db.refresh(note)
    
    return {
        "success": True,
        "note_id": note.note_id,
        "tags": note_update.tags
    }
```

#### Task 0.8.3: Add Tag Input to Frontend
**Files to Modify**: `frontend/src/components/NoteEditor.jsx`
```javascript
import React, { useState } from 'react'
import { Modal, Input, Select, Button, message, Tag } from 'antd'

const { TextArea } = Input

function NoteEditor({ note, visible, onClose, onSave }) {
  const [text, setText] = useState(note?.note_text || '')
  const [status, setStatus] = useState(note?.status || 'Open')
  const [tags, setTags] = useState(note?.tags || [])
  const [inputValue, setInputValue] = useState('')

  const handleAddTag = () => {
    if (inputValue && !tags.includes(inputValue)) {
      setTags([...tags, inputValue])
      setInputValue('')
    }
  }

  const handleRemoveTag = (removedTag) => {
    setTags(tags.filter(tag => tag !== removedTag))
  }

  const handleSave = async () => {
    try {
      const response = await fetch(`/api/v1/notes/${note.note_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ note_text: text, status, tags })
      })
      
      if (response.ok) {
        message.success('Note updated')
        onSave()
      }
    } catch (err) {
      message.error('Failed to update note')
    }
  }

  return (
    <Modal
      title="Edit Note"
      open={visible}
      onCancel={onClose}
      footer={[
        <Button key="cancel" onClick={onClose}>Cancel</Button>,
        <Button key="save" type="primary" onClick={handleSave}>Save</Button>
      ]}
    >
      <div style={{ marginBottom: '16px' }}>
        <label>Status:</label>
        <Select value={status} onChange={setStatus} style={{ width: '100%', marginTop: '8px' }}>
          <Select.Option value="Open">Open</Select.Option>
          <Select.Option value="In Progress">In Progress</Select.Option>
          <Select.Option value="Resolved">Resolved</Select.Option>
          <Select.Option value="Closed">Closed</Select.Option>
        </Select>
      </div>
      
      <div style={{ marginBottom: '16px' }}>
        <label>Tags:</label>
        <div style={{ marginTop: '8px' }}>
          {tags.map(tag => (
            <Tag key={tag} closable onClose={() => handleRemoveTag(tag)}>
              {tag}
            </Tag>
          ))}
        </div>
        <Input
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onPressEnter={handleAddTag}
          placeholder="Type and press Enter to add tag"
          style={{ marginTop: '8px' }}
        />
      </div>
      
      <div>
        <label>Note Text:</label>
        <TextArea 
          value={text}
          onChange={e => setText(e.target.value)}
          rows={4}
          style={{ marginTop: '8px' }}
        />
      </div>
    </Modal>
  )
}

export default NoteEditor
```

#### Task 0.8.4: Display Tags in Notes List
**Files to Modify**: `frontend/src/components/NotesList.jsx`
```javascript
// In the Card render, add tags display:
<Card>
  <Tag color="blue">{note.status}</Tag>
  <div style={{ marginTop: '8px' }}>{note.note_text}</div>
  {note.tags && note.tags.length > 0 && (
    <div style={{ marginTop: '8px' }}>
      {note.tags.map(tag => (
        <Tag key={tag} color="green">{tag}</Tag>
      ))}
    </div>
  )}
  <div style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
    {new Date(note.created_timestamp).toLocaleString()}
  </div>
</Card>
```

### Testing
```bash
# Rebuild
docker-compose down
docker-compose up --build -d

# Test editing a note and adding tags
# Tags should appear on notes
# Tags should be editable
```

### ✅ Definition of Done
- [ ] Can add multiple tags to note
- [ ] Tags shown on note cards
- [ ] Can edit and remove tags
- [ ] Tags saved to database
- [ ] Tags persist across sessions

---

## Version 0.9.0 - Primary Key Detection

**Goal**: Add actual CSV parsing with primary key detection

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Tasks

#### Task 0.9.1: Add pandas Dependency
**Files to Modify**: `backend/requirements.txt`
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-multipart==0.0.6
pandas==2.1.3
```

#### Task 0.9.2: Create CSV Processor
**Files to Create**: `backend/app/core/__init__.py` (empty)

**Files to Create**: `backend/app/core/csv_processor.py`
```python
import pandas as pd
from typing import Tuple, Optional

class CSVProcessor:
    @staticmethod
    def detect_primary_key(df: pd.DataFrame) -> Optional[str]:
        """Auto-detect primary key column"""
        id_candidates = ['id', 'ID', 'Id', 'primary_key', 'pk', 'key']
        
        for col in df.columns:
            if col.lower() in [c.lower() for c in id_candidates]:
                if df[col].is_unique and pd.api.types.is_integer_dtype(df[col]):
                    return col
        
        # Fallback: first numeric unique column
        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]) and df[col].is_unique:
                return col
        
        return None
    
    @staticmethod
    def validate_csv(df: pd.DataFrame, primary_key_col: str) -> Tuple[bool, str]:
        """Validate CSV structure"""
        if primary_key_col not in df.columns:
            return False, f"Column '{primary_key_col}' not found"
        
        if not df[primary_key_col].is_unique:
            return False, f"Column '{primary_key_col}' contains duplicates"
        
        if df[primary_key_col].isnull().any():
            return False, f"Column '{primary_key_col}' contains null values"
        
        return True, "Valid"
    
    @staticmethod
    def parse_csv(file_content: bytes) -> pd.DataFrame:
        """Parse CSV from bytes"""
        from io import BytesIO
        return pd.read_csv(BytesIO(file_content))
```

#### Task 0.9.3: Update CSV Import to Use Parser
**Files to Modify**: `backend/app/api/csv.py`
```python
from ..core.csv_processor import CSVProcessor
from ..models import CSVImport, CSVRow
import pandas as pd

@router.post("/import")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read file
    contents = await file.read()
    
    # Parse CSV
    df = CSVProcessor.parse_csv(contents)
    
    # Detect primary key
    primary_key = CSVProcessor.detect_primary_key(df)
    if not primary_key:
        return {
            "success": False,
            "error": "Could not detect primary key column",
            "columns": df.columns.tolist()
        }
    
    # Validate
    valid, msg = CSVProcessor.validate_csv(df, primary_key)
    if not valid:
        return {"success": False, "error": msg}
    
    # Create import record
    csv_import = CSVImport(
        filename=file.filename,
        row_count=len(df),
        primary_key_column=primary_key
    )
    db.add(csv_import)
    db.flush()
    
    # Store rows
    for _, row in df.iterrows():
        pk_value = int(row[primary_key])
        
        # Check if row exists
        existing = db.query(CSVRow).filter(
            CSVRow.primary_key_value == pk_value
        ).first()
        
        if not existing:
            csv_row = CSVRow(
                primary_key_value=pk_value,
                first_import_id=csv_import.import_id,
                last_seen_import_id=csv_import.import_id
            )
            db.add(csv_row)
    
    db.commit()
    
    return {
        "success": True,
        "import_id": csv_import.import_id,
        "filename": file.filename,
        "row_count": len(df),
        "primary_key": primary_key,
        "columns": df.columns.tolist()
    }

@router.post("/detect-key")
async def detect_primary_key(file: UploadFile = File(...)):
    contents = await file.read()
    df = CSVProcessor.parse_csv(contents)
    
    primary_key = CSVProcessor.detect_primary_key(df)
    
    return {
        "success": True,
        "detected_key": primary_key,
        "columns": df.columns.tolist()
    }
```

### Testing
```bash
# Create test CSV with proper ID column
echo -e "ID,Name,Value\n1,Test1,100\n2,Test2,200\n3,Test3,300" > test.csv

# Upload
curl -X POST -F "file=@test.csv" http://localhost:8080/api/v1/csv/import

# Check rows were created
sqlite3 data/notes.db "SELECT * FROM csv_rows;"
```

### ✅ Definition of Done
- [ ] CSV parsed with pandas
- [ ] Primary key auto-detected
- [ ] Rows inserted into csv_rows table
- [ ] Can detect various ID column names
- [ ] Returns list of columns

---

## Version 1.0.0 - MVP Complete

**Goal**: Polish MVP, add production Docker build, documentation

**Duration**: 4-5 hours  
**Review Time**: 15 minutes

### Tasks

#### Task 1.0.1: Create Production Dockerfile
**Files to Create**: `Dockerfile.prod`
```dockerfile
# Build frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Build backend
FROM python:3.10-alpine
WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY --from=frontend-build /app/dist ./app/static

RUN mkdir -p /app/data

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Task 1.0.2: Update Main App to Serve Frontend
**Files to Modify**: `backend/app/main.py`
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import engine, Base
from .api import csv, notes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="1.0.0")

app.include_router(csv.router, prefix="/api/v1/csv", tags=["CSV"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Notes"])

# Serve static frontend files
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/assets", StaticFiles(directory=str(static_path / "assets")), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse(str(static_path / "index.html"))

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}
```

#### Task 1.0.3: Production Docker Compose
**Files to Create**: `docker-compose.prod.yml`
```yaml
version: '3.8'

services:
  csv-notes:
    build:
      context: .
      dockerfile: Dockerfile.prod
    container_name: csv-notes-manager
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=sqlite:///./data/notes.db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8080/api/v1/health')"]
      interval: 30s
      timeout: 3s
      retries: 3
```

#### Task 1.0.4: Update README
**Files to Modify**: `README.md`
```markdown
# CSV Notes Manager

Version: 1.0.0 (MVP)

A web application for managing persistent notes on CSV file rows across multiple file versions.

## Features

✅ CSV file import with auto-detection of primary key
✅ Create, read, update notes on CSV rows  
✅ Add multiple tags to notes
✅ Note status management (Open, In Progress, Resolved, Closed)
✅ Docker deployment
✅ SQLite database with data persistence

## Quick Start

### Production Deployment (Docker)

```bash
# Start the application
docker-compose -f docker-compose.prod.yml up -d

# Application available at: http://localhost:8080
```

### Development Setup

```bash
# Start development environment with hot reload
docker-compose -f docker-compose.dev.yml up

# Frontend: http://localhost:3000
# Backend: http://localhost:8080
# API Docs: http://localhost:8080/docs
```

## Usage

1. **Import CSV**: Upload a CSV file with an ID column
2. **View Rows**: Enter a row ID to see its notes
3. **Add Notes**: Create notes with text, status, and tags
4. **Edit Notes**: Click Edit to modify note content

## API Endpoints

- `POST /api/v1/csv/import` - Import CSV file
- `GET /api/v1/csv/imports` - List imports
- `POST /api/v1/notes/` - Create note
- `GET /api/v1/notes/by-row/{row_id}` - Get notes for row
- `PUT /api/v1/notes/{note_id}` - Update note

Full API documentation: http://localhost:8080/docs

## Data Persistence

All data stored in `./data/notes.db` (SQLite database)

Backup your data:
```bash
cp data/notes.db data/notes.db.backup
```

## Technology Stack

- **Backend**: Python 3.10, FastAPI, SQLAlchemy, pandas
- **Frontend**: React 18, Ant Design, Vite
- **Database**: SQLite 3
- **Deployment**: Docker, Docker Compose

## Roadmap

- [ ] Orphaned row detection
- [ ] Advanced filtering
- [ ] Custom views
- [ ] Export functionality
- [ ] Multi-user support

## License

MIT
```

### Testing
```bash
# Build production version
docker-compose -f docker-compose.prod.yml build

# Run
docker-compose -f docker-compose.prod.yml up -d

# Test complete workflow:
# 1. Visit http://localhost:8080
# 2. Upload CSV via API
# 3. View notes in UI
# 4. Create and edit notes

# Verify data persists
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
# Data should still be there
```

### ✅ Definition of Done
- [ ] Production Docker build works
- [ ] Frontend served from backend
- [ ] All features working end-to-end
- [ ] Data persists across restarts
- [ ] README complete and accurate
- [ ] Can deploy with single command

---

## Version 1.1.0 - Orphaned Rows

**Goal**: Detect and mark orphaned rows on re-import

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Key Tasks
- Modify CSV import to detect missing rows
- Mark rows as orphaned
- Add "Deleted Items" view
- Show orphaned indicator in UI

---

## Version 1.2.0 - Basic Filters

**Goal**: Filter by status and tags

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Key Tasks
- Add filter panel component
- Implement backend filter logic
- Status filter (multi-select)
- Tag filter (multi-select)

---

## Version 1.3.0 - Custom Views

**Goal**: Save and load custom filter/column configurations

**Duration**: 4-5 hours  
**Review Time**: 12 minutes

### Key Tasks
- Add user_views table support
- Create view management UI
- Save current view configuration
- Load saved views

---

## Version 1.4.0 - Export Functionality

**Goal**: Export current view as CSV

**Duration**: 3-4 hours  
**Review Time**: 10 minutes

### Key Tasks
- Add export endpoints
- Generate CSV from filtered data
- Include notes in export
- Download functionality

---

## Version 1.5.0 - Production Ready

**Goal**: Final polish and deployment artifacts

**Duration**: 4-5 hours  
**Review Time**: 15 minutes

### Key Tasks
- PyInstaller build script
- Error handling improvements
- Loading states
- Comprehensive documentation
- Deployment guide

---

## Release Checklist

For each version release:

### Pre-Release
- [ ] All tests passing
- [ ] Manual testing complete
- [ ] Documentation updated
- [ ] CHANGELOG entry added
- [ ] Version numbers bumped

### Release Process
- [ ] Create git tag: `git tag v0.X.0`
- [ ] Build Docker image: `docker build -t csv-notes:v0.X.0 .`
- [ ] Test deployment from scratch
- [ ] Verify all endpoints working
- [ ] Verify data persistence

### Post-Release
- [ ] Tag pushed to repository
- [ ] Docker image published (if applicable)
- [ ] Release notes created
- [ ] Users notified of new version

---

## Development Guidelines

> **📋 Note**: For complete contribution guidelines, including commit message conventions, branching strategy, and PR process, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

### Git Workflow

**Branch Strategy**: All changes **must** start in a separate branch. Direct commits to `main` are not allowed.

```bash
# Start new feature (create branch from main)
git checkout main
git pull origin main
git checkout -b feature/note-editing

# Make changes and commit using Conventional Commits format
git add .
git commit -m "feat(notes): add note editing functionality"
git push origin feature/note-editing

# Create Pull Request, get approval, then merge to main

# After merge to main, create version tag and release
git checkout main
git pull origin main
git tag v0.7.0
git push origin main --tags

# Create GitHub Release for the tag
```

**Commit Message Format** (Conventional Commits):
```
<type>(<scope>): <subject>

Examples:
feat(csv-import): add auto-detection of primary key
fix(notes): resolve duplicate tag creation
docs(readme): update installation instructions
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for complete details on:
- Conventional commit types and scopes
- Branch naming conventions
- Pull request process
- Version management and releases

### Testing Before Commit
```bash
# Backend tests
cd backend
pytest

# Build Docker
docker-compose build

# Smoke test
docker-compose up -d
curl http://localhost:8080/api/v1/health
docker-compose down
```

### Code Review Checklist
- [ ] Code follows project structure
- [ ] No hardcoded values (use environment variables)
- [ ] Error handling present
- [ ] Logging added for key operations
- [ ] Documentation strings added
- [ ] README updated if needed
- [ ] Increment results in working, deployable version

---

## Deployment Scenarios

### Scenario 1: Local Development
```bash
docker-compose -f docker-compose.dev.yml up
```
- Frontend hot reload on port 3000
- Backend hot reload on port 8080
- Database in ./data/

### Scenario 2: Production (Single Server)
```bash
docker-compose -f docker-compose.prod.yml up -d
```
- Single container with backend + frontend
- Port 8080 exposed
- Data volume mounted

### Scenario 3: Production (Separate Services)
```yaml
# docker-compose.prod-advanced.yml
services:
  backend:
    build: ./backend
    expose:
      - "8080"
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
  
  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
```

---

## Troubleshooting Guide

### Issue: Docker container won't start
```bash
# Check logs
docker-compose logs

# Common fixes:
# 1. Port already in use
docker-compose down
lsof -i :8080  # Kill process using port

# 2. Volume permission issues
sudo chown -R $USER:$USER ./data
```

### Issue: Database locked
```bash
# Stop all containers
docker-compose down

# Remove lock file
rm data/notes.db-shm
rm data/notes.db-wal

# Restart
docker-compose up -d
```

### Issue: Frontend not connecting to backend
```bash
# Check CORS settings in backend
# Verify proxy configuration in vite.config.js
# Check network in docker-compose
```

---

## Summary

This incremental plan delivers:

✅ **Small Steps**: Each version is 2-4 hours of focused work  
✅ **Always Working**: Every version is deployable and testable  
✅ **Easy Review**: Changes are small and focused  
✅ **Docker First**: Container deployment from v0.1.0  
✅ **Clear Progress**: 15 versions from Hello World to Full MVP  

**Total Time to MVP (v1.0.0)**: ~30-40 hours  
**Total Time to Production (v1.5.0)**: ~50-65 hours

Each step builds upon the previous one, ensuring the application is always in a working state and can be deployed at any point.