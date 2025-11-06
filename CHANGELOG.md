# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed
- Notes page defaults to showing all notes with an optional row filter

### Deprecated

### Removed

### Fixed

### Security

---

## [0.6.0] - 2025-11-09

### Added
- Ant Design UI components for browsing notes within the frontend
- Row selector input for loading notes tied to a specific CSV row
- Read-only notes list that surfaces status tags and timestamps

### Changed

### Deprecated

### Removed

### Fixed

### Security

---

## [0.5.0] - 2025-11-08

### Added
- SQLAlchemy models for CSV rows and notes with relationships
- FastAPI endpoints for creating notes and retrieving notes by row

### Changed
- Application version metadata updated to 0.5.0 across backend and frontend
- Health endpoint response streamlined for the notes-enabled release

---

## [0.4.0] - 2025-11-07

### Added
- Vite-powered React frontend that displays backend health status
- Development Docker Compose configuration with frontend hot reloading

### Changed
- FastAPI application metadata updated to version 0.4.0

---

## [0.3.0] - 2025-11-06

### Added
- CSV import API endpoints with file metadata persistence in SQLite
- SQLAlchemy model updates supporting CSV import tracking

### Changed
- FastAPI application metadata updated to version 0.3.0 with CSV routes

---

## [0.2.0] - 2025-11-05

### Added
- SQLAlchemy configuration and session management for SQLite database support
- Initial `CSVImport` ORM model for tracking imported files
- Docker Compose volume and environment configuration for database persistence

### Changed
- FastAPI application version updated to 0.2.0 with database-aware health check

---

## [0.1.0] - 2025-11-04

### Added
- Project documentation structure
- Development plan with incremental versioning
- Technical architecture specification
- Software requirements specification
- README with quick start guide
- Contributing guidelines
- Conventional commits setup
- GitHub PR template
- CHANGELOG template

### Changed
- Updated development-plan.md to reference CONTRIBUTING.md
- Updated architecture.md with git workflow guidelines

---

## How to Update This Changelog

When making changes to the project:

1. **Add your changes under `[Unreleased]`** in the appropriate section:
   - `Added` for new features
   - `Changed` for changes in existing functionality
   - `Deprecated` for soon-to-be removed features
   - `Removed` for now removed features
   - `Fixed` for any bug fixes
   - `Security` for vulnerability fixes

2. **Use descriptive entries** that explain what changed and why:
   ```markdown
   ### Added
   - CSV import with auto-detection of primary key column
   - Support for multiple tags per note
   ```

3. **Link to issues/PRs** when applicable:
   ```markdown
   ### Fixed
   - Resolved duplicate tag creation issue ([#42](../../issues/42))
   ```

4. **When releasing a new version**:
   - Move entries from `[Unreleased]` to a new version section
   - Add the version number and release date
   - Follow semantic versioning (MAJOR.MINOR.PATCH)
   - Create a git tag and GitHub release

### Example Release Entry

```markdown
## [1.0.0] - 2025-12-01

### Added
- Complete CSV import functionality with validation
- Note management with CRUD operations
- Tag system for note categorization
- Status tracking (Open, In Progress, Resolved, Closed)
- React frontend with Ant Design components
- Docker deployment configuration

### Changed
- Improved CSV parsing performance by 50%
- Updated database schema to support orphaned rows

### Fixed
- Fixed memory leak in CSV import process
- Resolved race condition in note updates

### Security
- Added input validation for all API endpoints
- Implemented SQL injection prevention
```

---

## Version History

**Legend:**
- 🎉 Major release
- ✨ Minor release (new features)
- 🐛 Patch release (bug fixes)

---

<!-- 
Template for new releases:

## [X.Y.Z] - YYYY-MM-DD

### Added
- Feature description

### Changed
- Change description

### Deprecated
- Deprecation notice

### Removed
- Removal notice

### Fixed
- Bug fix description

### Security
- Security fix description

-->