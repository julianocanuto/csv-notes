# CSV Notes Manager - Software Specification

## 1. Executive Summary

### 1.1 Project Overview
A local web application that allows users to maintain persistent notes on CSV file rows across multiple file versions. Notes are linked via a primary key (ID) and stored in a local SQLite database, eliminating the need to copy/paste data between CSV versions.

### 1.2 Key Features
- Import CSV files (weekly/daily frequency, ~2000 rows, 25 columns)
- Add multiple time-stamped notes per row with free-form tags
- Track notes across CSV versions using numeric ID as primary key
- Manage orphaned notes when rows are deleted from CSV
- Customizable views with filtering and search capabilities
- Export functionality for filtered data and reports
- Single executable deployment with local web interface

---

## 2. Business Requirements

### 2.1 Problem Statement
Users receive updated CSV files regularly (weekly/daily) where rows can be added or deleted without notice. They need to maintain notes on specific rows that persist across file versions without manual data migration.

### 2.2 Success Criteria
- Zero data loss when importing new CSV versions
- Notes remain accessible even when source rows are deleted
- Quick access to notes via primary key lookup
- Ability to track note history over time
- Simple deployment (single .exe file)

---

## 3. Functional Requirements

### 3.1 CSV Import Management

#### 3.1.1 File Import
- **Action**: User uploads/imports CSV file via web interface
- **Processing**:
  - Auto-detect primary key column (looks for column named "ID" or similar)
  - Allow manual column selection if auto-detection fails or is incorrect
  - Remember primary key column choice for subsequent imports
  - Parse CSV with 25 columns and ~2000 rows
  - Store CSV metadata: filename, import timestamp
  
#### 3.1.2 Change Detection
- **Action**: Compare new CSV against current database state
- **Detection Logic**:
  - Identify new rows (IDs not in database)
  - Identify deleted rows (IDs in database but not in new CSV)
  - Identify unchanged rows (IDs present in both)
- **User Feedback**: Display import summary
  - "Import complete: X new rows added, Y rows deleted, Z rows with notes are now orphaned"

#### 3.1.3 Orphaned Row Management
- **Trigger**: When a row with notes is not present in new CSV
- **Behavior**:
  - Mark row as "orphaned" in database
  - Retain all notes and history
  - Display orphaned status in UI with warning indicator
  - Keep orphaned rows visible in "Deleted Items" view

### 3.2 Note Management

#### 3.2.1 Note Creation
- **Location**: Expandable section within table row
- **Required Fields**:
  - Note text (multi-line text input)
  - Tags (free-form, comma-separated, multiple allowed)
  - Status (dropdown: Open, In Progress, Resolved, Closed)
- **Auto-generated Fields**:
  - Timestamp (date and time of creation)
  - CSV source (filename and import date)
  - Note ID (internal unique identifier)

#### 3.2.2 Note Editing
- **Capability**: Full edit access to all note fields
- **Fields Editable**: Note text, tags, status
- **Fields Immutable**: Timestamp, CSV source, Note ID
- **Tracking**: Store modification timestamp (last edited date/time)

#### 3.2.3 Note Deletion
- **Action**: Soft delete (mark as deleted, retain in database)
- **UI Behavior**: Remove from view immediately
- **Data Retention**: Keep for potential audit/recovery

#### 3.2.4 Note Display
- **Primary View**: Notes collapsed by default in table row
- **Expansion**: Click row to expand and show all notes for that ID
- **Note List Display**:
  - Sort chronologically (newest first)
  - Show: timestamp, text preview, tags, status
  - Click individual note to view/edit full details
- **Never Use**: Modal/popup windows for note display

### 3.3 View Management

#### 3.3.1 Custom Views
- **User-Configurable Elements**:
  - **Column Selection**: Choose which of 25 CSV columns to display
  - **Filters**: Apply multiple filters simultaneously
    - By tags (multi-select)
    - By status (multi-select: Open, In Progress, Resolved, Closed)
    - By date range (note creation/modification dates)
    - Show only rows with notes (checkbox)
    - Show only orphaned rows (checkbox)
    - Search by specific ID
    - Full-text search within note text
  - **Sort Order**: 
    - Primary sort column
    - Sort direction (ascending/descending)
    - Secondary sort column (optional)
- **View Persistence**: Save custom views by name for reuse

#### 3.3.2 Predefined Views
1. **All Data**
   - Display all rows from current CSV
   - Include both active and orphaned rows
   - No filters applied by default
   
2. **Deleted Items**
   - Display only orphaned rows
   - Show when row was last present in CSV
   - Show all associated notes

### 3.4 Search and Filter

#### 3.4.1 Tag-Based Search
- **Input**: Multi-select tag filter
- **Logic**: Show rows with notes matching ANY selected tag (OR logic)
- **Display**: Highlight matching tags in results

#### 3.4.2 Status Filter
- **Input**: Multi-select status checkboxes
- **Options**: Open, In Progress, Resolved, Closed
- **Logic**: Show rows with notes matching ANY selected status

#### 3.4.3 Date Range Filter
- **Input**: Start date and end date pickers
- **Logic**: Filter by note creation or modification timestamp
- **Preset Options**: Last 7 days, Last 30 days, Custom range

#### 3.4.4 Text Search
- **Input**: Search text box
- **Scope**: Search within note text content
- **Behavior**: Case-insensitive partial match

#### 3.4.5 ID Search
- **Input**: Numeric ID text box
- **Behavior**: Jump to specific row by primary key

### 3.5 Export Functionality

#### 3.5.1 Export Current View
- **Format**: CSV file
- **Content**: 
  - All visible columns from current view
  - Additional columns for notes (concatenated with timestamps)
  - Respects current filters and sort order
- **Filename**: `export_[view_name]_[timestamp].csv`

#### 3.5.2 Export Notes by ID
- **Input**: Specific ID number
- **Format**: PDF or CSV report
- **Content**:
  - All CSV data for that ID
  - Complete note history with timestamps
  - Tags and status for each note
  - CSV source information
- **Filename**: `notes_report_ID[number]_[timestamp].pdf`

#### 3.5.3 Export Orphaned Items
- **Format**: CSV file
- **Content**:
  - All orphaned rows with their data
  - All notes for each orphaned row
  - Last seen date (when row was last in CSV)
- **Filename**: `orphaned_items_[timestamp].csv`

---

## 4. Technical Architecture

### 4.1 Technology Stack

#### 4.1.1 Backend
- **Language**: Python 3.10+
- **Web Framework**: Flask or FastAPI (recommendation: **FastAPI** for modern async support and automatic API documentation)
- **Database**: SQLite 3
- **ORM**: SQLAlchemy
- **CSV Processing**: pandas
- **Packaging**: PyInstaller (create single .exe)

#### 4.1.2 Frontend
- **Framework**: React.js or Vue.js (recommendation: **React** for component reusability)
- **UI Library**: Material-UI or Ant Design (recommendation: **Ant Design** for enterprise-grade tables)
- **State Management**: Redux Toolkit or Zustand
- **HTTP Client**: Axios
- **Build Tool**: Vite
- **CSS**: Tailwind CSS or component library styles

#### 4.1.3 Development Tools
- **API Testing**: Pytest
- **Frontend Testing**: Jest, React Testing Library
- **Code Quality**: Black (formatter), Flake8 (linter)
- **Version Control**: Git

### 4.2 Database Schema

#### 4.2.1 Tables

**csv_imports**
```sql
CREATE TABLE csv_imports (
    import_id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    import_timestamp DATETIME NOT NULL,
    row_count INTEGER NOT NULL,
    primary_key_column TEXT NOT NULL
);
```

**csv_rows**
```sql
CREATE TABLE csv_rows (
    row_id INTEGER PRIMARY KEY AUTOINCREMENT,
    primary_key_value INTEGER NOT NULL,
    first_import_id INTEGER NOT NULL,
    last_seen_import_id INTEGER NOT NULL,
    is_orphaned BOOLEAN DEFAULT FALSE,
    orphaned_date DATETIME,
    csv_data JSON NOT NULL,  -- Store all 25 columns as JSON
    FOREIGN KEY (first_import_id) REFERENCES csv_imports(import_id),
    FOREIGN KEY (last_seen_import_id) REFERENCES csv_imports(import_id),
    UNIQUE(primary_key_value)
);
```

**notes**
```sql
CREATE TABLE notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    row_id INTEGER NOT NULL,
    note_text TEXT NOT NULL,
    status TEXT CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')) NOT NULL,
    created_timestamp DATETIME NOT NULL,
    modified_timestamp DATETIME,
    created_by_user_id INTEGER,  -- NULL for now, used for future multi-user
    csv_import_id INTEGER NOT NULL,  -- Which CSV was active when note was created
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (row_id) REFERENCES csv_rows(row_id),
    FOREIGN KEY (csv_import_id) REFERENCES csv_imports(import_id),
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)  -- Future
);
```

**note_tags**
```sql
CREATE TABLE note_tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER NOT NULL,
    tag_name TEXT NOT NULL,
    FOREIGN KEY (note_id) REFERENCES notes(note_id),
    INDEX idx_tag_name (tag_name)
);
```

**user_views**
```sql
CREATE TABLE user_views (
    view_id INTEGER PRIMARY KEY AUTOINCREMENT,
    view_name TEXT NOT NULL,
    user_id INTEGER,  -- NULL for now, used for future multi-user
    view_config JSON NOT NULL,  -- Stores column selection, filters, sort order
    is_predefined BOOLEAN DEFAULT FALSE,
    created_timestamp DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)  -- Future
);
```

**users** (Future multi-user support)
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_timestamp DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### 4.2.2 Indexes
```sql
CREATE INDEX idx_csv_rows_primary_key ON csv_rows(primary_key_value);
CREATE INDEX idx_csv_rows_orphaned ON csv_rows(is_orphaned);
CREATE INDEX idx_notes_row_id ON notes(row_id);
CREATE INDEX idx_notes_status ON notes(status);
CREATE INDEX idx_notes_created ON notes(created_timestamp);
CREATE INDEX idx_note_tags_name ON note_tags(tag_name);
```

### 4.3 API Endpoints

#### 4.3.1 CSV Management
- `POST /api/csv/import` - Upload and process CSV file
- `GET /api/csv/imports` - List all CSV imports with metadata
- `GET /api/csv/current` - Get current CSV data with pagination
- `GET /api/csv/columns` - Get list of available columns
- `POST /api/csv/detect-primary-key` - Auto-detect primary key column
- `PUT /api/csv/set-primary-key` - Manually set primary key column

#### 4.3.2 Note Management
- `POST /api/notes` - Create new note
- `GET /api/notes/:noteId` - Get specific note
- `PUT /api/notes/:noteId` - Update note
- `DELETE /api/notes/:noteId` - Soft delete note
- `GET /api/notes/by-row/:rowId` - Get all notes for a row
- `GET /api/tags` - Get all unique tags (autocomplete)

#### 4.3.3 View Management
- `GET /api/views` - List all views
- `POST /api/views` - Create custom view
- `GET /api/views/:viewId` - Get view configuration
- `PUT /api/views/:viewId` - Update view
- `DELETE /api/views/:viewId` - Delete view
- `POST /api/views/:viewId/apply` - Apply view and get filtered data

#### 4.3.4 Search and Filter
- `POST /api/search` - Search with filters (tags, status, date, text, ID)
- `GET /api/rows/orphaned` - Get all orphaned rows

#### 4.3.5 Export
- `POST /api/export/view` - Export current view as CSV
- `GET /api/export/notes/:primaryKey` - Export notes report for specific ID
- `GET /api/export/orphaned` - Export orphaned items

### 4.4 Application Architecture

#### 4.4.1 Component Structure
```
┌─────────────────────────────────────────┐
│          Single .exe File               │
│  (PyInstaller bundle)                   │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  Python Backend                │    │
│  │  - FastAPI/Flask Web Server    │    │
│  │  - SQLAlchemy ORM              │    │
│  │  - Business Logic              │    │
│  │  - CSV Processing              │    │
│  └────────────────────────────────┘    │
│              ↕                          │
│  ┌────────────────────────────────┐    │
│  │  SQLite Database               │    │
│  │  (data.db file)                │    │
│  └────────────────────────────────┘    │
│              ↕                          │
│  ┌────────────────────────────────┐    │
│  │  Static Frontend Files         │    │
│  │  - React SPA (bundled)         │    │
│  │  - HTML/CSS/JS                 │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
              ↕
    http://localhost:8080
              ↕
┌─────────────────────────────────────────┐
│       User's Web Browser                │
│  (Chrome, Firefox, Edge)                │
└─────────────────────────────────────────┘
```

#### 4.4.2 Startup Flow
1. User double-clicks .exe file
2. Application checks if port 8080 is available (try 8081, 8082 if occupied)
3. Initialize SQLite database (create if not exists)
4. Start web server on localhost
5. Automatically open default browser to http://localhost:8080
6. Display system tray icon with "Stop Server" option

#### 4.4.3 Data Flow - CSV Import
```
User uploads CSV
    ↓
Frontend sends file to /api/csv/import
    ↓
Backend validates file format
    ↓
Auto-detect primary key column (with manual override option)
    ↓
Parse CSV with pandas
    ↓
For each row:
    - Check if primary_key_value exists in csv_rows
    - If exists: update last_seen_import_id, set is_orphaned=FALSE
    - If new: insert into csv_rows
    ↓
Identify orphaned rows (not in new CSV but in database)
    ↓
Set is_orphaned=TRUE and orphaned_date for missing rows
    ↓
Generate import summary statistics
    ↓
Return summary to frontend
    ↓
Display success message with statistics
```

#### 4.4.4 Data Flow - Note Management
```
User clicks row to expand
    ↓
Frontend requests /api/notes/by-row/:rowId
    ↓
Backend queries notes and note_tags tables
    ↓
Return all notes with tags, sorted by timestamp
    ↓
Display notes in expandable section
    ↓
User adds/edits note
    ↓
Frontend sends to /api/notes (POST or PUT)
    ↓
Backend validates data
    ↓
Insert/update notes table
    ↓
Insert/update note_tags table
    ↓
Return updated note data
    ↓
Refresh note list in UI
```

### 4.5 Future Multi-User Architecture Considerations

**Design Decisions for Future Scalability:**

1. **Database Schema**: Already includes `users` table and `user_id` foreign keys (currently NULL)
2. **Authentication Layer**: Space in architecture for JWT token-based auth
3. **API Structure**: RESTful design allows easy addition of auth middleware
4. **Row-Level Permissions**: Can add `created_by` fields to track ownership
5. **Deployment Path**:
   - Phase 1: Local .exe (current spec)
   - Phase 2: Deploy backend to company server (Docker container)
   - Phase 3: Add authentication and user management
   - Phase 4: Multi-tenant if needed for different departments

**Migration Path:**
- SQLite database can be migrated to PostgreSQL with minimal code changes (SQLAlchemy abstraction)
- Frontend requires no changes (API contract remains same)
- Add authentication middleware in backend
- Implement user registration/login UI components

---

## 5. User Interface Design

### 5.1 Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Header                                                      │
│  [Logo] CSV Notes Manager        [Import CSV] [User: Admin] │
├─────────────────────────────────────────────────────────────┤
│  Navigation Bar                                              │
│  [All Data] [Deleted Items] [Custom Views ▼]                │
├─────────────────────────────────────────────────────────────┤
│  Toolbar                                                     │
│  Columns: [☐ Col1 ☑ Col2 ☑ Col3...] | Filters: [+Add]     │
│  Tags: [tag1 ×] [tag2 ×]  Status: [Open] [In Progress]     │
│  [Search: _______] [Export ▼]                               │
├─────────────────────────────────────────────────────────────┤
│  Data Table (Main Content Area)                             │
│  ┌───┬────────┬─────────┬─────────┬──────┬──────┬────────┐ │
│  │ ▼ │ ID     │ Column2 │ Column3 │ ... │ Notes│ Status │ │
│  ├───┼────────┼─────────┼─────────┼──────┼──────┼────────┤ │
│  │ ▸ │ 17487  │ Value A │ Value B │ ... │ 3    │ Active │ │
│  ├───┼────────┼─────────┼─────────┼──────┼──────┼────────┤ │
│  │ ▾ │ 17488  │ Value C │ Value D │ ... │ 5    │ ⚠Orph  │ │
│  │   │ ┌─────────────────────────────────────────────────┐ │
│  │   │ │ Notes for ID 17488                              │ │
│  │   │ │ ┌─────────────────────────────────────────────┐ │ │
│  │   │ │ │ [Open] Oct 1, 2025 3:45 PM                  │ │ │
│  │   │ │ │ This item needs follow-up next week         │ │ │
│  │   │ │ │ Tags: urgent, follow-up                     │ │ │
│  │   │ │ │ [Edit] [Delete]                             │ │ │
│  │   │ │ └─────────────────────────────────────────────┘ │ │
│  │   │ │ ┌─────────────────────────────────────────────┐ │ │
│  │   │ │ │ [Resolved] Sep 28, 2025 10:22 AM            │ │ │
│  │   │ │ │ Issue has been resolved                     │ │ │
│  │   │ │ │ Tags: resolved                              │ │ │
│  │   │ │ │ [Edit] [Delete]                             │ │ │
│  │   │ │ └─────────────────────────────────────────────┘ │ │
│  │   │ │ [+ Add New Note]                                │ │
│  │   │ └─────────────────────────────────────────────────┘ │
│  ├───┼────────┼─────────┼─────────┼──────┼──────┼────────┤ │
│  │ ▸ │ 17489  │ Value E │ Value F │ ... │ 1    │ Active │ │
│  └───┴────────┴─────────┴─────────┴──────┴──────┴────────┘ │
│                                                              │
│  Showing 1-50 of 2000 rows    [< Prev] [Next >]            │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Key UI Components

#### 5.2.1 Import Dialog
- Drag-and-drop CSV file upload
- File name and size display
- Primary key column selector (auto-detected, with dropdown to change)
- "Remember this column" checkbox
- Import button with progress indicator

#### 5.2.2 Import Summary Modal (after import completes)
```
┌──────────────────────────────────────┐
│ Import Successful                 ✓  │
├──────────────────────────────────────┤
│ File: weekly_data_2025_10_03.csv    │
│ Imported: Oct 3, 2025 2:15 PM       │
│                                      │
│ Summary:                             │
│ • 150 new rows added                 │
│ • 23 rows deleted                    │
│ • 1,827 rows unchanged               │
│ • 5 deleted rows had notes           │
│   (now marked as orphaned)           │
│                                      │
│ [View Orphaned Items] [Close]        │
└──────────────────────────────────────┘
```

#### 5.2.3 Note Editor (inline in expanded row)
```
┌─────────────────────────────────────────┐
│ Add Note for ID 17488                   │
├─────────────────────────────────────────┤
│ Note Text:                              │
│ ┌─────────────────────────────────────┐ │
│ │                                     │ │
│ │ (multi-line text area)              │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Tags (comma separated):                 │
│ [urgent, follow-up, customer_issue___] │
│                                         │
│ Status: [Open ▼]                        │
│                                         │
│ [Cancel] [Save Note]                    │
└─────────────────────────────────────────┘
```

#### 5.2.4 Filter Panel
```
┌─────────────────────────────────────┐
│ Active Filters                      │
├─────────────────────────────────────┤
│ Tags:         [urgent ×] [+Add]     │
│ Status:       [☑ Open]              │
│               [☑ In Progress]       │
│               [☐ Resolved]          │
│               [☐ Closed]            │
│ Date Range:   [Last 7 days ▼]      │
│ Show only:    [☑ Has notes]         │
│               [☐ Orphaned only]     │
│                                     │
│ [Clear All] [Save as View]          │
└─────────────────────────────────────┘
```

#### 5.2.5 Custom View Selector
```
Dropdown menu:
┌─────────────────────────────────┐
│ Predefined Views                │
│ • All Data                      │
│ • Deleted Items                 │
├─────────────────────────────────┤
│ My Custom Views                 │
│ • Active Work Items             │
│ • High Priority                 │
│ • Resolved Last Week            │
├─────────────────────────────────┤
│ [+ Create New View]             │
└─────────────────────────────────┘
```

### 5.3 Visual Indicators

#### 5.3.1 Row Status
- **Active Row**: Normal styling (white/light gray background)
- **Orphaned Row**: Yellow/amber warning background with ⚠ icon
- **Row with Notes**: Note count badge (e.g., "3" in circle)
- **Expanded Row**: Blue highlight border

#### 5.3.2 Note Status Colors
- **Open**: Blue dot/badge
- **In Progress**: Orange dot/badge
- **Resolved**: Green dot/badge
- **Closed**: Gray dot/badge

#### 5.3.3 Tag Display
- Rounded pill-shaped badges
- Distinct colors for visual separation
- Consistent color per tag name (hash-based color assignment)

### 5.4 Responsive Behavior
- Minimum width: 1024px (laptop screen)
- Collapsible sidebar for filters on smaller screens
- Horizontal scroll for table if many columns selected
- Pagination for performance (50 rows per page default, adjustable)

---

## 6. Non-Functional Requirements

### 6.1 Performance
- CSV import: < 5 seconds for 2000 rows
- Page load: < 2 seconds for initial view
- Note creation: < 500ms response time
- Table pagination: < 1 second per page
- Search/filter: < 2 seconds for complex queries

### 6.2 Reliability
- Data integrity: ACID transactions for all database operations
- Crash recovery: Auto-save work in progress
- Database backup: Manual export option for entire database

### 6.3 Usability
- Zero-installation deployment (single .exe)
- Intuitive UI requiring no training for basic operations
- Keyboard shortcuts for common actions
- Undo capability for note deletion (soft delete with recovery)

### 6.4 Security
- Local-only access (no external network exposure)
- File system permissions: Database file write protection
- Future: Password-protected access when multi-user enabled
- Input validation: Sanitize all user inputs to prevent SQL injection

### 6.5 Maintainability
- Modular code structure for easy updates
- Comprehensive inline documentation
- Logging: Application logs for debugging (rotating file log)
- Version tracking: Semantic versioning (X.Y.Z)

### 6.6 Scalability Considerations
- Database design supports multi-user from day one
- API structure allows future remote deployment
- Performance optimization for up to 10,000 rows
- Tag system supports unlimited unique tags

---

## 7. Implementation Phases

### Phase 1: Core Functionality (MVP)
**Timeline: 4-6 weeks**

**Deliverables:**
1. Database schema implementation
2. CSV import with auto-detect primary key
3. Basic note CRUD operations (Create, Read, Update, Delete)
4. Simple web UI with table display
5. Expandable row for notes
6. Tag system
7. Note status management
8. "All Data" predefined view

**Success Criteria:**
- Can import CSV and view data
- Can add, edit, delete notes on rows
- Notes persist across CSV imports
- Single .exe deployment works

### Phase 2: Advanced Features
**Timeline: 3-4 weeks**

**Deliverables:**
1. Orphaned row detection and management
2. "Deleted Items" predefined view
3. Custom view creation and management
4. Advanced filtering (tags, status, date, text search)
5. Column show/hide functionality
6. Sort functionality
7. Import summary notifications

**Success Criteria:**
- Full filter/search capabilities working
- Custom views save and load correctly
- Orphaned rows clearly indicated

### Phase 3: Export & Polish
**Timeline: 2-3 weeks**

**Deliverables:**
1. Export current view to CSV
2. Export notes report by ID
3. Export orphaned items
4. UI/UX refinements
5. Performance optimizations
6. Error handling improvements
7. User documentation

**Success Criteria:**
- All export formats working correctly
- Application feels polished and responsive
- Edge cases handled gracefully

### Phase 4: Testing & Deployment
**Timeline: 1-2 weeks**

**Deliverables:**
1. Comprehensive testing (unit, integration, E2E)
2. Bug fixes
3. Final .exe packaging with PyInstaller
4. Installation guide
5. User manual
6. Version 1.0 release

**Success Criteria:**
- Zero critical bugs
- Successful deployment on target machines
- User acceptance testing passed

---

## 8. Future Enhancements (Post-MVP)

### 8.1 Multi-User Support
- User authentication (login/logout)
- User management interface
- User-specific views
- Note author attribution
- Permission levels (viewer, editor, admin)

### 8.2 Collaboration Features
- Note comments/replies
- @mention notifications
- Note assignment to users
- Activity feed

### 8.3 Advanced Analytics
- Dashboard with statistics
- Note trends over time
- Tag frequency analysis
- CSV change history visualization

### 8.4 Integration & Automation
- Email notifications for specific triggers
- Scheduled CSV imports from network location
- API webhooks for external systems
- CSV template validation

### 8.5 Enhanced Export
- PDF reports with charts
- Excel export with formatting
- Custom report templates

---

## 9. Technical Specifications

### 9.1 Development Environment Setup

**Prerequisites:**
- Python 3.10 or higher
- Node.js 18+ and npm
- Git

**Backend Setup:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pandas python-multipart aiofiles
pip install pytest black flake8 pyinstaller
```

**Frontend Setup:**
```bash
cd frontend
npm create vite@latest . -- --template react
npm install axios antd @reduxjs/toolkit react-redux
npm install -D tailwindcss postcss autoprefixer
```

### 9.2 Project Structure
```
csv-notes-manager/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry
│   │   ├── database.py          # Database connection & session
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas for API
│   │   ├── crud.py              # Database operations
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── csv.py           # CSV endpoints
│   │   │   ├── notes.py         # Note endpoints
│   │   │   ├── views.py         # View management endpoints
│   │   │   ├── search.py        # Search/filter endpoints
│   │   │   └── export.py        # Export endpoints
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── csv_processor.py # CSV parsing logic
│   │   │   └── export_utils.py  # Export generation
│   │   └── config.py            # Configuration settings
│   ├── tests/
│   │   ├── test_csv.py
│   │   ├── test_notes.py
│   │   └── test_api.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DataTable.jsx    # Main table component
│   │   │   ├── NoteEditor.jsx   # Note creation/editing
│   │   │   ├── FilterPanel.jsx  # Filtering UI
│   │   │   ├── ImportDialog.jsx # CSV upload
│   │   │   ├── ViewSelector.jsx # View management
│   │   │   └── ExportMenu.jsx   # Export options
│   │   ├── store/
│   │   │   ├── store.js         # Redux store
│   │   │   ├── csvSlice.js
│   │   │   ├── notesSlice.js
│   │   │   └── viewsSlice.js
│   │   ├── api/
│   │   │   └── client.js        # Axios configuration
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   └── notes.db                 # SQLite database (generated)
│
├── build_exe.py                 # PyInstaller build script
├── README.md
└── LICENSE
```

### 9.3 Build Configuration

**PyInstaller Spec File (build.spec):**
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['backend/app/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend/dist'),  # Include built React app
        ('data', 'data'),
    ],
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.protocols',
        'sqlalchemy.sql.default_comparator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CSVNotesManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Application icon
)
```

**Build Script (build_exe.py):**
```python
import subprocess
import sys
import os
import shutil

def build_frontend():
    """Build React frontend"""
    print("Building frontend...")
    os.chdir('frontend')
    subprocess.run(['npm', 'install'], check=True)
    subprocess.run(['npm', 'run', 'build'], check=True)
    os.chdir('..')
    print("Frontend build complete!")

def build_exe():
    """Build executable with PyInstaller"""
    print("Building executable...")
    subprocess.run([
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'build.spec'
    ], check=True)
    print("Executable build complete!")
    print(f"Output: {os.path.abspath('dist/CSVNotesManager.exe')}")

if __name__ == '__main__':
    try:
        build_frontend()
        build_exe()
        print("\n✓ Build successful!")
        print("Executable location: dist/CSVNotesManager.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)
```

### 9.4 Key Code Examples

#### 9.4.1 Database Models (backend/app/models.py)
```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CSVImport(Base):
    __tablename__ = 'csv_imports'
    
    import_id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    import_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    row_count = Column(Integer, nullable=False)
    primary_key_column = Column(String, nullable=False)
    
    rows = relationship("CSVRow", back_populates="first_import", foreign_keys="CSVRow.first_import_id")
    notes = relationship("Note", back_populates="csv_import")

class CSVRow(Base):
    __tablename__ = 'csv_rows'
    
    row_id = Column(Integer, primary_key=True, autoincrement=True)
    primary_key_value = Column(Integer, nullable=False, unique=True, index=True)
    first_import_id = Column(Integer, ForeignKey('csv_imports.import_id'), nullable=False)
    last_seen_import_id = Column(Integer, ForeignKey('csv_imports.import_id'), nullable=False)
    is_orphaned = Column(Boolean, default=False, index=True)
    orphaned_date = Column(DateTime, nullable=True)
    csv_data = Column(JSON, nullable=False)  # All 25 columns as JSON
    
    first_import = relationship("CSVImport", foreign_keys=[first_import_id])
    last_seen_import = relationship("CSVImport", foreign_keys=[last_seen_import_id])
    notes = relationship("Note", back_populates="row", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = 'notes'
    
    note_id = Column(Integer, primary_key=True, autoincrement=True)
    row_id = Column(Integer, ForeignKey('csv_rows.row_id'), nullable=False, index=True)
    note_text = Column(Text, nullable=False)
    status = Column(String, nullable=False)  # Open, In Progress, Resolved, Closed
    created_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    modified_timestamp = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    created_by_user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)  # Future
    csv_import_id = Column(Integer, ForeignKey('csv_imports.import_id'), nullable=False)
    is_deleted = Column(Boolean, default=False)
    
    row = relationship("CSVRow", back_populates="notes")
    csv_import = relationship("CSVImport", back_populates="notes")
    tags = relationship("NoteTag", back_populates="note", cascade="all, delete-orphan")
    user = relationship("User", back_populates="notes")  # Future

class NoteTag(Base):
    __tablename__ = 'note_tags'
    
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    note_id = Column(Integer, ForeignKey('notes.note_id'), nullable=False)
    tag_name = Column(String, nullable=False, index=True)
    
    note = relationship("Note", back_populates="tags")

class UserView(Base):
    __tablename__ = 'user_views'
    
    view_id = Column(Integer, primary_key=True, autoincrement=True)
    view_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)  # Future
    view_config = Column(JSON, nullable=False)
    is_predefined = Column(Boolean, default=False)
    created_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    user = relationship("User", back_populates="views")  # Future

class User(Base):
    """Future multi-user support"""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    notes = relationship("Note", back_populates="user")
    views = relationship("UserView", back_populates="user")
```

#### 9.4.2 CSV Import Logic (backend/app/utils/csv_processor.py)
```python
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime

class CSVProcessor:
    @staticmethod
    def detect_primary_key_column(df: pd.DataFrame) -> str:
        """Auto-detect primary key column"""
        # Look for common ID column names
        id_candidates = ['id', 'ID', 'Id', 'primary_key', 'pk', 'key']
        
        for col in df.columns:
            if col.lower() in [c.lower() for c in id_candidates]:
                if df[col].is_unique and pd.api.types.is_integer_dtype(df[col]):
                    return col
        
        # Fallback: first numeric unique column
        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]) and df[col].is_unique:
                return col
        
        raise ValueError("No suitable primary key column found")
    
    @staticmethod
    def validate_csv(df: pd.DataFrame, primary_key_col: str) -> Tuple[bool, str]:
        """Validate CSV structure"""
        if primary_key_col not in df.columns:
            return False, f"Column '{primary_key_col}' not found in CSV"
        
        if not df[primary_key_col].is_unique:
            return False, f"Column '{primary_key_col}' contains duplicate values"
        
        if df[primary_key_col].isnull().any():
            return False, f"Column '{primary_key_col}' contains null values"
        
        return True, "Valid"
    
    @staticmethod
    def process_import(
        df: pd.DataFrame, 
        primary_key_col: str,
        existing_rows: Dict[int, int]  # {primary_key_value: row_id}
    ) -> Dict:
        """Process CSV import and generate change summary"""
        current_keys = set(df[primary_key_col].astype(int).values)
        existing_keys = set(existing_rows.keys())
        
        new_keys = current_keys - existing_keys
        deleted_keys = existing_keys - current_keys
        unchanged_keys = current_keys & existing_keys
        
        # Prepare row data
        new_rows = []
        for idx, row in df[df[primary_key_col].isin(new_keys)].iterrows():
            new_rows.append({
                'primary_key_value': int(row[primary_key_col]),
                'csv_data': row.to_dict()
            })
        
        return {
            'new_rows': new_rows,
            'new_count': len(new_keys),
            'deleted_keys': list(deleted_keys),
            'deleted_count': len(deleted_keys),
            'unchanged_count': len(unchanged_keys),
            'total_rows': len(df)
        }
```

#### 9.4.3 FastAPI Main Application (backend/app/main.py)
```python
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import webbrowser
import threading
import os
from pathlib import Path

from .api import csv, notes, views, search, export
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSV Notes Manager", version="1.0.0")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(csv.router, prefix="/api/csv", tags=["CSV"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(views.router, prefix="/api/views", tags=["Views"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])

# Serve React frontend
frontend_path = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

def open_browser(port: int):
    """Open browser after short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{port}")

def start_server(port: int = 8080):
    """Start the web server"""
    # Open browser in separate thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Start server
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")

if __name__ == "__main__":
    start_server()
```

#### 9.4.4 React Data Table Component (frontend/src/components/DataTable.jsx)
```javascript
import React, { useState, useEffect } from 'react';
import { Table, Tag, Button, Space } from 'antd';
import { DownOutlined, RightOutlined, WarningOutlined } from '@ant-design/icons';
import NotesList from './NotesList';
import axios from 'axios';

const DataTable = ({ viewConfig, filters }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedRowKeys, setExpandedRowKeys] = useState([]);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 50 });

  useEffect(() => {
    fetchData();
  }, [viewConfig, filters, pagination.current]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/search', {
        filters: filters,
        page: pagination.current,
        page_size: pagination.pageSize,
        columns: viewConfig.columns,
        sort: viewConfig.sort
      });
      setData(response.data.rows);
      setPagination(prev => ({ ...prev, total: response.data.total }));
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const expandedRowRender = (record) => {
    return <NotesList rowId={record.row_id} primaryKey={record.primary_key_value} />;
  };

  const columns = [
    {
      title: '',
      key: 'expand',
      width: 50,
      render: (_, record) => (
        expandedRowKeys.includes(record.row_id) ? <DownOutlined /> : <RightOutlined />
      ),
    },
    {
      title: 'ID',
      dataIndex: ['csv_data', 'ID'],
      key: 'id',
      width: 100,
      sorter: true,
    },
    ...viewConfig.columns.map(col => ({
      title: col,
      dataIndex: ['csv_data', col],
      key: col,
      ellipsis: true,
    })),
    {
      title: 'Notes',
      key: 'notes_count',
      width: 80,
      render: (_, record) => (
        record.note_count > 0 ? (
          <Tag color="blue">{record.note_count}</Tag>
        ) : null
      ),
    },
    {
      title: 'Status',
      key: 'status',
      width: 100,
      render: (_, record) => (
        record.is_orphaned ? (
          <Tag icon={<WarningOutlined />} color="warning">Orphaned</Tag>
        ) : (
          <Tag color="success">Active</Tag>
        )
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={data}
      loading={loading}
      rowKey="row_id"
      pagination={pagination}
      onChange={(newPagination, filters, sorter) => {
        setPagination(newPagination);
      }}
      expandable={{
        expandedRowRender,
        expandedRowKeys,
        onExpand: (expanded, record) => {
          setExpandedRowKeys(expanded ? [record.row_id] : []);
        },
        expandIcon: () => null, // Custom expand icon in first column
      }}
    />
  );
};

export default DataTable;
```

---

## 10. Testing Strategy

### 10.1 Unit Tests

**Backend Unit Tests:**
- Database models (CRUD operations)
- CSV processing logic
- Primary key detection algorithm
- Export generation functions
- Filter query builder

**Frontend Unit Tests:**
- Component rendering
- Redux state management
- API client functions
- Filter logic
- View configuration parsing

### 10.2 Integration Tests

**API Integration Tests:**
- CSV import flow (upload → process → store)
- Note creation with tags
- Search with multiple filters
- View save and load
- Export generation

**Database Integration Tests:**
- Transaction rollback on error
- Foreign key constraints
- Orphaned row marking
- Concurrent note updates

### 10.3 End-to-End Tests

**User Workflow Tests:**
1. Import CSV → View data → Add notes
2. Import new CSV → Verify orphaned rows
3. Create custom view → Save → Load
4. Apply filters → Export results
5. Edit note → Verify changes persist

### 10.4 Performance Tests

**Load Testing:**
- Import CSV with 10,000 rows
- Search with 1000 notes
- Render table with all columns visible
- Export large filtered dataset

**Benchmarks:**
- CSV import: < 10 seconds for 10,000 rows
- Search response: < 2 seconds with complex filters
- Table pagination: < 1 second
- Note save: < 500ms

### 10.5 User Acceptance Testing

**Test Scenarios:**
1. Daily workflow simulation (1 week of imports)
2. Edge cases (empty CSV, missing primary key)
3. Usability testing with target users
4. Cross-browser compatibility (Chrome, Firefox, Edge)

---

## 11. Deployment Guide

### 11.1 Building the Executable

**Step 1: Prepare Environment**
```bash
# Clone repository
git clone <repository-url>
cd csv-notes-manager

# Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

**Step 2: Build**
```bash
# Run build script
python build_exe.py
```

**Step 3: Test Executable**
```bash
# Run from dist folder
cd dist
./CSVNotesManager.exe
```

### 11.2 Distribution

**Package Contents:**
- `CSVNotesManager.exe` (main executable)
- `README.txt` (quick start guide)
- `LICENSE.txt`

**Installation:**
1. Copy `CSVNotesManager.exe` to desired location
2. Double-click to run
3. Application creates `data/notes.db` on first run
4. Browser opens automatically to http://localhost:8080

### 11.3 Uninstallation

**Manual Uninstall:**
1. Close application (system tray → Stop Server)
2. Delete `CSVNotesManager.exe`
3. Delete `data` folder to remove all notes (optional)

### 11.4 Backup and Recovery

**Manual Backup:**
- Copy `data/notes.db` file to safe location
- Backup recommended before major CSV imports

**Recovery:**
- Replace `data/notes.db` with backup copy
- Restart application

**Export-Based Backup:**
- Use "Export All Data" feature periodically
- Keeps human-readable CSV backups

---

## 12. User Documentation Outline

### 12.1 Quick Start Guide

**Getting Started in 5 Minutes:**
1. Launch CSVNotesManager.exe
2. Click "Import CSV" button
3. Select your CSV file
4. Confirm or adjust primary key column
5. Start adding notes to rows

### 12.2 Feature Documentation

**Importing CSV Files:**
- Supported formats and requirements
- Primary key column selection
- Understanding import summary

**Working with Notes:**
- Adding your first note
- Using tags effectively
- Note status workflow
- Editing and deleting notes

**Managing Views:**
- Creating custom views
- Using predefined views
- Column selection
- Saving and loading views

**Filtering and Search:**
- Filter by tags
- Filter by status
- Date range filters
- Text search
- Combining multiple filters

**Exporting Data:**
- Export current view
- Export notes by ID
- Export orphaned items
- Understanding export formats

**Handling Orphaned Rows:**
- What are orphaned rows?
- Why rows become orphaned
- Working with deleted items
- Cleaning up old orphaned rows

### 12.3 Troubleshooting

**Common Issues:**
- Port 8080 already in use → Application tries 8081, 8082
- CSV won't import → Check primary key column
- Notes not showing → Check filters
- Browser doesn't open → Manually navigate to localhost:8080
- Application won't close → Use system tray icon

**Error Messages:**
- "No suitable primary key found" → Manual column selection needed
- "Duplicate primary key values" → CSV has duplicate IDs
- "Database locked" → Close other instances

---

## 13. Maintenance and Support

### 13.1 Version Updates

**Semantic Versioning:**
- **Major (X.0.0)**: Breaking changes, database schema changes
- **Minor (1.X.0)**: New features, backwards compatible
- **Patch (1.0.X)**: Bug fixes, minor improvements

**Update Process:**
1. Backup `data/notes.db`
2. Download new version
3. Replace executable
4. Run database migrations if needed (automated)

### 13.2 Database Migrations

**Migration Strategy:**
- Use Alembic for schema versioning
- Auto-run migrations on application start
- Backup before migration
- Rollback capability

**Example Migration (future):**
```python
# versions/002_add_user_table.py
def upgrade():
    op.create_table('users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        # ...
    )
    
def downgrade():
    op.drop_table('users')
```

### 13.3 Logging and Debugging

**Log Locations:**
- Application logs: `logs/app.log`
- Error logs: `logs/errors.log`
- Import logs: `logs/imports.log`

**Log Levels:**
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Operation failures
- DEBUG: Detailed debugging (development only)

**Debug Mode:**
```bash
# Enable debug logging
CSVNotesManager.exe --debug
```

### 13.4 Performance Monitoring

**Metrics to Track:**
- CSV import duration
- Database query times
- Memory usage
- Note count per row
- Total database size

**Optimization Recommendations:**
- Archive old orphaned rows (> 1 year)
- Limit note text to 10,000 characters
- Use pagination (don't load all 2000 rows at once)
- Index frequently searched columns

---

## 14. Security Considerations

### 14.1 Current Security (Single-User, Local)

**File System Security:**
- Database file permissions (user read/write only)
- No network exposure (localhost only)
- Input validation on all user inputs

**Data Protection:**
- SQL injection prevention (SQLAlchemy parameterized queries)
- XSS prevention (React escapes output by default)
- CSRF protection (not needed for localhost)

### 14.2 Future Security (Multi-User)

**Authentication:**
- Password hashing (bcrypt with salt)
- JWT tokens for session management
- Token expiration (24 hours)
- Secure password requirements

**Authorization:**
- Role-based access control (Admin, Editor, Viewer)
- Row-level permissions
- Note ownership validation

**Network Security:**
- HTTPS/TLS encryption
- Rate limiting on API endpoints
- CORS configuration for allowed domains
- SQL injection protection (already implemented)

**Audit Trail:**
- Log all note modifications
- Track user actions
- Failed login attempts
- Data export tracking

---

## 15. Success Metrics

### 15.1 Development Metrics

**Code Quality:**
- Test coverage > 80%
- No critical security vulnerabilities
- Code review approval for all changes
- Documentation completeness

**Performance:**
- 95% of operations complete within SLA
- Zero data loss incidents
- Application startup < 3 seconds
- Memory usage < 500MB with 10,000 rows

### 15.2 User Adoption Metrics

**Usage:**
- Daily active users
- Average notes per user per day
- CSV import frequency
- Custom views created

**Satisfaction:**
- User satisfaction survey (target > 4/5)
- Bug report frequency
- Feature request quantity and quality
- Time to complete common tasks

### 15.3 Business Impact

**Efficiency Gains:**
- Time saved vs manual copy/paste (estimated)
- Reduction in data loss incidents
- Improved data tracking accuracy
- Faster decision-making with historical notes

---

## 16. Risks and Mitigation

### 16.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Data corruption in SQLite | High | Low | Regular backups, transaction integrity |
| CSV format incompatibility | Medium | Medium | Robust parsing with error handling |
| Performance degradation (>10k rows) | Medium | Medium | Pagination, indexing, query optimization |
| Port conflict on user machine | Low | Medium | Auto-detect available ports |
| Browser compatibility issues | Low | Low | Test on major browsers, use standard APIs |

### 16.2 User Adoption Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Users resist new workflow | High | Medium | Simple UI, comprehensive training docs |
| Learning curve too steep | Medium | Low | Intuitive design, quick start guide |
| Missing critical features | Medium | Medium | MVP validation with target users |
| Performance perceived as slow | Medium | Low | Optimize critical paths, show loading states |

### 16.3 Future Expansion Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Database migration complexity | High | Medium | Design schema with future in mind |
| Multi-user concurrency issues | High | High | Proper locking, transaction handling |
| Server hosting costs | Medium | Low | Start with self-hosted, cloud optional |
| Authentication security flaws | High | Medium | Use proven libraries, security audit |

---

## 17. Glossary

**CSV**: Comma-Separated Values - A file format for tabular data

**Primary Key**: A unique identifier for each row (e.g., ID column)

**Orphaned Row**: A row that existed in a previous CSV but is missing from the latest import

**Note**: A timestamped comment attached to a specific row via its primary key

**Tag**: A free-form label attached to a note for categorization

**View**: A saved configuration of columns, filters, and sort order

**SQLite**: A lightweight, file-based relational database

**FastAPI**: Modern Python web framework for building APIs

**React**: JavaScript library for building user interfaces

**PyInstaller**: Tool for packaging Python applications as executables

**SPA**: Single Page Application - Web app that loads once and updates dynamically

**CRUD**: Create, Read, Update, Delete - Basic database operations

**ORM**: Object-Relational Mapping - Database abstraction layer (SQLAlchemy)

---

## 18. Appendices

### Appendix A: Sample CSV Structure

```csv
ID,Customer_Name,Order_Date,Amount,Status,Region,Product,Quantity,Notes_Field,Priority
17487,Acme Corp,2025-10-01,1500.00,Pending,North,Widget A,50,Urgent delivery,High
17488,Beta Inc,2025-10-02,2300.00,Shipped,South,Widget B,75,Standard,Medium
17489,Gamma LLC,2025-10-03,890.00,Completed,East,Widget C,25,Follow-up needed,Low
```

### Appendix B: API Response Examples

**CSV Import Response:**
```json
{
  "success": true,
  "import_id": 42,
  "summary": {
    "filename": "weekly_data_2025_10_03.csv",
    "import_timestamp": "2025-10-03T14:30:00Z",
    "new_rows": 150,
    "deleted_rows": 23,
    "unchanged_rows": 1827,
    "orphaned_rows_with_notes": 5,
    "total_rows": 2000
  }
}
```

**Note Creation Response:**
```json
{
  "note_id": 1234,
  "row_id": 567,
  "primary_key_value": 17487,
  "note_text": "Customer requested expedited shipping",
  "status": "Open",
  "tags": ["urgent", "shipping", "customer-request"],
  "created_timestamp": "2025-10-03T14:35:22Z",
  "csv_import_id": 42,
  "csv_filename": "weekly_data_2025_10_03.csv"
}
```

### Appendix C: Database Size Estimates

| Rows | Notes/Row | Avg Note Size | Est. DB Size |
|------|-----------|---------------|--------------|
| 2,000 | 3 | 200 chars | ~5 MB |
| 10,000 | 3 | 200 chars | ~25 MB |
| 50,000 | 3 | 200 chars | ~125 MB |
| 100,000 | 5 | 300 chars | ~500 MB |

*Note: Estimates include indexes and metadata. Actual size may vary.*

### Appendix D: Keyboard Shortcuts (Recommended)

| Shortcut | Action |
|----------|--------|
| Ctrl + I | Import CSV |
| Ctrl + N | Add new note to selected row |
| Ctrl + F | Focus search box |
| Ctrl + E | Export current view |
| Ctrl + S | Save current view |
| Escape | Close expanded row |
| Enter | Expand/collapse selected row |
| Ctrl + , | Open settings |

### Appendix E: Configuration File (config.json)

```json
{
  "application": {
    "name": "CSV Notes Manager",
    "version": "1.0.0",
    "port": 8080,
    "port_range": [8080, 8081, 8082, 8083, 8084]
  },
  "database": {
    "path": "data/notes.db",
    "backup_on_startup": true,
    "auto_vacuum": true
  },
  "csv": {
    "max_file_size_mb": 100,
    "encoding": "utf-8",
    "delimiter_auto_detect": true,
    "remember_primary_key": true
  },
  "ui": {
    "default_page_size": 50,
    "max_page_size": 500,
    "theme": "light",
    "date_format": "YYYY-MM-DD HH:mm:ss"
  },
  "notes": {
    "max_text_length": 10000,
    "max_tags_per_note": 10,
    "statuses": ["Open", "In Progress", "Resolved", "Closed"]
  },
  "export": {
    "output_directory": "exports",
    "filename_timestamp_format": "YYYYMMDD_HHmmss",
    "pdf_page_size": "A4"
  },
  "logging": {
    "level": "INFO",
    "file_path": "logs/app.log",
    "max_file_size_mb": 10,
    "backup_count": 5
  }
}
```

### Appendix F: Technology Alternatives Considered

#### Backend Framework Comparison

| Framework | Pros | Cons | Decision |
|-----------|------|------|----------|
| **FastAPI** ✓ | Modern, async, auto docs, fast | Newer, smaller ecosystem | **Selected** |
| Flask | Mature, simple, large community | Synchronous, manual docs | Alternative |
| Django | Full-featured, admin panel, ORM | Heavyweight for this use case | Not selected |

#### Frontend Framework Comparison

| Framework | Pros | Cons | Decision |
|-----------|------|------|----------|
| **React** ✓ | Large ecosystem, component reuse | Requires state management | **Selected** |
| Vue.js | Simpler learning curve, integrated state | Smaller ecosystem | Alternative |
| Svelte | Smallest bundle, fast | Smaller ecosystem, fewer libraries | Not selected |

#### Database Comparison

| Database | Pros | Cons | Decision |
|----------|------|------|----------|
| **SQLite** ✓ | Serverless, single file, zero config | Not for concurrent writes | **Selected** |
| PostgreSQL | Robust, concurrent, full-featured | Requires server, complex setup | Future option |
| MongoDB | Flexible schema, JSON-native | NoSQL, overkill for this | Not selected |

#### UI Component Library Comparison

| Library | Pros | Cons | Decision |
|---------|------|------|----------|
| **Ant Design** ✓ | Enterprise tables, complete components | Larger bundle size | **Selected** |
| Material-UI | Material Design, popular | Complex customization | Alternative |
| Chakra UI | Modern, accessible | Fewer data components | Not selected |

---

## 19. Prompt for Software Development

### 19.1 Complete Development Prompt

You can use this prompt with an AI coding assistant or development team:

```
Create a CSV Notes Manager application with the following specifications:

OVERVIEW:
- Local web application (Python backend + React frontend)
- Manages persistent notes on CSV file rows across versions
- Notes linked via numeric primary key (ID column)
- Single .exe deployment using PyInstaller
- SQLite database for storage

CORE FEATURES:
1. CSV Import
   - Upload CSV files (~2000 rows, 25 columns)
   - Auto-detect primary key column with manual override
   - Track changes between versions (new/deleted rows)
   - Mark deleted rows as "orphaned" while preserving notes

2. Note Management
   - Add multiple timestamped notes per row
   - Note fields: text, free-form tags (multiple), status (Open/In Progress/Resolved/Closed)
   - Edit and delete notes (soft delete)
   - Display notes in expandable table rows (never use modals)
   - Track which CSV version note was created under

3. View Management
   - Customizable views: column selection, filters, sort order
   - Predefined views: "All Data" and "Deleted Items"
   - Save custom views by name

4. Search & Filter
   - Filter by: tags (multi-select), status, date range, ID, note text
   - Show only rows with notes
   - Show only orphaned rows

5. Export
   - Export current filtered view to CSV
   - Export all notes for specific ID as report
   - Export all orphaned items

TECH STACK:
- Backend: Python 3.10+, FastAPI, SQLAlchemy, pandas, PyInstaller
- Frontend: React, Ant Design, Redux Toolkit, Axios, Vite
- Database: SQLite 3
- Deployment: Single .exe that launches local web server on localhost:8080

DATABASE SCHEMA:
- csv_imports: import_id, filename, import_timestamp, row_count, primary_key_column
- csv_rows: row_id, primary_key_value (unique), first_import_id, last_seen_import_id, is_orphaned, orphaned_date, csv_data (JSON)
- notes: note_id, row_id, note_text, status, created_timestamp, modified_timestamp, created_by_user_id (NULL for now), csv_import_id, is_deleted
- note_tags: tag_id, note_id, tag_name
- user_views: view_id, view_name, user_id (NULL for now), view_config (JSON), is_predefined, created_timestamp
- users: (future multi-user support - include schema but don't implement auth yet)

KEY REQUIREMENTS:
- Architecture must support future multi-user expansion
- Show import summary after each CSV upload
- Expandable table rows for notes (no modals/popups)
- Remember primary key column choice
- Performance: <5s import for 2000 rows, <2s for searches
- Auto-open browser when .exe launches

UI LAYOUT:
- Header with Import button
- Navigation bar with view selector
- Toolbar with column selector, filters, search, export
- Main data table with expandable rows
- Pagination (50 rows per page)

Please implement this application following the technical architecture specified, including all API endpoints, database models, React components, and build configuration for PyInstaller.
```

### 19.2 Phase-by-Phase Development Prompts

**Phase 1 Prompt (MVP):**
```
Implement Phase 1 (MVP) of CSV Notes Manager:
- Database setup with SQLAlchemy models
- CSV import API with auto-detect primary key
- Basic note CRUD operations (create, read, update, delete)
- Simple React UI with Ant Design table
- Expandable rows showing notes
- Tag system and status dropdown
- "All Data" view
- Basic .exe build with PyInstaller

Success criteria: Can import CSV, view data, add/edit/delete notes with tags and status
```

**Phase 2 Prompt (Advanced Features):**
```
Implement Phase 2 of CSV Notes Manager:
- Orphaned row detection on CSV import
- "Deleted Items" view
- Custom view creation and persistence
- Advanced filtering: tags, status, date range, text search
- Column show/hide functionality
- Sort functionality
- Import summary notification

Success criteria: Full filter/search working, custom views save/load, orphaned rows visible
```

**Phase 3 Prompt (Export & Polish):**
```
Implement Phase 3 of CSV Notes Manager:
- Export current view to CSV
- Export notes report by ID (PDF/CSV)
- Export orphaned items list
- UI/UX refinements and error handling
- Performance optimizations for large datasets
- Comprehensive logging

Success criteria: All exports working, polished UI, handles edge cases gracefully
```

---

## 20. Project Timeline

### 20.1 Detailed Timeline (10-13 weeks total)

```
Week 1-2: Setup & Phase 1 Foundation
├─ Week 1: Project setup, database models, API structure
├─ Week 2: CSV import logic, basic React components

Week 3-4: Phase 1 Core Features
├─ Week 3: Note CRUD operations, tag system
├─ Week 4: UI integration, expandable rows, basic styling

Week 5-6: Phase 1 Completion & Testing
├─ Week 5: Testing, bug fixes, PyInstaller configuration
├─ Week 6: MVP testing, documentation, Phase 1 delivery

Week 7-8: Phase 2 Advanced Features
├─ Week 7: Orphaned row detection, custom views backend
├─ Week 8: Filter/search implementation, custom views UI

Week 9: Phase 2 Polish
├─ Column management, sort, import summary
├─ Testing and bug fixes

Week 10-11: Phase 3 Export Features
├─ Week 10: CSV export, notes report generation
├─ Week 11: PDF export, UI refinements

Week 12: Testing & Documentation
├─ Comprehensive testing (unit, integration, E2E)
├─ User documentation, deployment guide

Week 13: Final Release
├─ Bug fixes, performance optimization
├─ Final build and release (v1.0.0)
```

### 20.2 Milestones

| Milestone | Week | Deliverable |
|-----------|------|-------------|
| **M1: Project Setup** | 1 | Repository, database, API skeleton |
| **M2: MVP Alpha** | 4 | Basic functionality working locally |
| **M3: MVP Beta** | 5 | Single .exe deployment working |
| **M4: Phase 1 Complete** | 6 | Stable MVP ready for user testing |
| **M5: Phase 2 Complete** | 9 | Advanced features implemented |
| **M6: Phase 3 Complete** | 11 | All export features working |
| **M7: Release Candidate** | 12 | Fully tested, documented |
| **M8: v1.0.0 Release** | 13 | Production-ready release |

---

## 21. Post-Release Roadmap

### 21.1 Version 1.1 (Month 2-3)
- **User feedback integration**: Address top 5 user requests
- **Performance improvements**: Optimize for 20,000+ rows
- **Bulk operations**: Bulk note creation, bulk status update
- **Note templates**: Predefined note templates for common scenarios
- **Dark mode**: UI theme toggle

### 21.2 Version 1.5 (Month 4-6)
- **Advanced search**: Regular expressions, fuzzy search
- **Note attachments**: Attach small files to notes (images, PDFs)
- **Audit log**: Complete history of all changes
- **Keyboard shortcuts**: Full keyboard navigation
- **Column formulas**: Simple calculations on CSV columns

### 21.3 Version 2.0 (Month 7-12)
- **Multi-user support**: User authentication and permissions
- **Web deployment**: Deploy to company server
- **Real-time collaboration**: Multiple users editing simultaneously
- **Email notifications**: Configurable alerts
- **API for integrations**: REST API for external systems
- **Mobile responsive**: Optimized mobile UI

### 21.4 Version 3.0 (Year 2)
- **Advanced analytics**: Dashboards, trend analysis
- **Workflow automation**: Automated note creation rules
- **Integration plugins**: Slack, Teams, email clients
- **Custom fields**: User-defined metadata on notes
- **AI-assisted features**: Auto-categorization, sentiment analysis

---

## 22. Cost Estimate (Development)

### 22.1 Development Costs (Estimated)

| Role | Hours | Rate | Cost |
|------|-------|------|------|
| Backend Developer | 200 | $80/hr | $16,000 |
| Frontend Developer | 180 | $75/hr | $13,500 |
| UI/UX Designer | 40 | $70/hr | $2,800 |
| QA Engineer | 60 | $60/hr | $3,600 |
| Project Manager | 40 | $90/hr | $3,600 |
| **Total** | **520** | - | **$39,500** |

*Note: Costs vary significantly based on location, experience, and team structure. This is a rough estimate for a professional development team.*

### 22.2 Alternative: Solo Developer

| Phase | Hours | Estimated Time |
|-------|-------|----------------|
| Phase 1 (MVP) | 160 | 4-6 weeks |
| Phase 2 (Advanced) | 120 | 3-4 weeks |
| Phase 3 (Export) | 80 | 2-3 weeks |
| Testing & Docs | 60 | 1-2 weeks |
| **Total** | **420** | **10-15 weeks** |

### 22.3 Ongoing Costs

| Item | Frequency | Cost |
|------|-----------|------|
| Maintenance (bug fixes) | Monthly | $500-1000 |
| Feature updates | Quarterly | $2000-5000 |
| Support | As needed | $50-100/hr |

*For purely local use: $0 infrastructure costs*
*For company-wide deployment: $50-200/month cloud hosting*

---

## 23. Legal and Compliance

### 23.1 Licensing
- **Application License**: MIT or proprietary (company decision)
- **Third-party Dependencies**: All use permissive licenses (MIT, Apache 2.0, BSD)
- **No GPL conflicts**: Careful library selection for commercial use

### 23.2 Data Privacy
- **Local Storage**: All data stays on user's machine (GDPR compliant by design)
- **No Telemetry**: No data collection or phone-home features
- **User Control**: Full control over data export and deletion

### 23.3 Future Compliance (Multi-User)
- **GDPR**: Right to access, right to deletion, data portability
- **SOC 2**: Implement when deploying company-wide
- **Data Retention**: Configurable retention policies for notes
- **Audit Logs**: Track all data access and modifications

---

## 24. Conclusion

This specification provides a comprehensive blueprint for building a CSV Notes Manager that:

✅ **Solves the core problem**: Maintains persistent notes across CSV versions without manual copy/paste

✅ **Scales gracefully**: Designed for single-user local use with clear path to multi-user enterprise deployment

✅ **User-friendly**: Intuitive web interface with customizable views and powerful search capabilities

✅ **Technically sound**: Modern tech stack, robust database design, performance-optimized

✅ **Future-proof**: Architecture supports planned enhancements without major rewrites

### Next Steps:
1. **Validate requirements** with target users
2. **Set up development environment** and repository
3. **Begin Phase 1 implementation** (MVP)
4. **Iterate based on user feedback**
5. **Plan for company-wide rollout** after successful pilot

### Key Success Factors:
- Start simple (MVP) and iterate
- Get user feedback early and often
- Maintain clean, documented codebase
- Test thoroughly at each phase
- Document everything for future maintenance

This specification can be used as a living document throughout development, updated as requirements evolve and new insights emerge.

---

**Document Version**: 1.0  
**Last Updated**: October 3, 2025  
**Status**: Ready for Development