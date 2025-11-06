# CSV Notes Manager

**Version:** 0.5.0 (In Development)
**Status:** 🚧 Under Active Development

A web application for managing persistent notes on CSV file rows across multiple file versions.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Technology Stack](#technology-stack)
- [Project Status](#project-status)
- [License](#license)

---

## Overview

CSV Notes Manager is a web application that will allow you to maintain persistent notes on specific CSV file rows across multiple versions of the file. Notes are linked via a primary key (ID column) and are stored in a local SQLite database, eliminating the need to manually track information between file updates. Version **0.5.0** introduces the first backend endpoints for creating notes tied to imported CSV rows, expanding on the frontend and database foundations delivered in earlier releases.

### Use Case

Ideal for scenarios where you:
- Receive regular CSV file updates (daily/weekly)
- Need to track notes on specific rows
- Want notes to persist even when rows are deleted from the CSV
- Need to maintain historical context across file versions

---

## Features

### Current Features (v0.5.0)

✅ FastAPI backend with welcome and health-check endpoints
✅ CSV import API with persistence of upload metadata
✅ SQLite database managed via SQLAlchemy ORM
✅ React 18 frontend (Vite) that displays backend health information
✅ Note API supporting creation and retrieval of notes for CSV rows
✅ Dockerfile and docker-compose setup with persistent data volume
✅ Docker Compose development environment with hot-reloading frontend and backend
✅ Project documentation outlining roadmap and contribution process

### Planned Features

- 📝 CSV file import with auto-detection of primary key
- 📌 Create, read, update, and delete notes on CSV rows
- 🏷️ Multiple tags per note for categorization
- 📊 Note status management (Open, In Progress, Resolved, Closed)
- 🔍 Advanced filtering and search capabilities
- 👁️ Custom views with saved configurations
- 📤 Export functionality for notes and filtered data
- ⚠️ Orphaned row detection and management

See [`development-plan.md`](development-plan.md) for the complete feature roadmap.

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd csv-notes

# Create a Python virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

### Running with Docker (Recommended)

```bash
# Build and start the FastAPI service
docker-compose up --build
```

The API will be available at **http://localhost:8080**.

To stop the containers:

```bash
docker-compose down
```

### Running the Full Development Environment

```bash
docker-compose -f docker-compose.dev.yml up
```

- Frontend available at **http://localhost:3000**
- Backend available at **http://localhost:8080**
- Hot reload enabled for both services

### Running Locally Without Docker

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Access the Application

- **Frontend UI**: http://localhost:3000/
- **Root Endpoint**: http://localhost:8080/
- **Health Check**: http://localhost:8080/api/v1/health
- **Interactive API Docs**: http://localhost:8080/docs

---

## Documentation

| Document | Description |
|----------|-------------|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | **Start here!** Contribution guidelines, commit conventions, and PR process |
| [`development-plan.md`](development-plan.md) | Incremental development roadmap with detailed implementation steps |
| [`architecture.md`](architecture.md) | Technical architecture, database schema, and design decisions |
| [`csv-notes-spec.md`](csv-notes-spec.md) | Complete software specification and requirements |

---

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting any changes.

### Quick Contribution Guide

1. **Fork and clone** the repository
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our [coding standards](CONTRIBUTING.md#code-style-guidelines)
4. **Commit using [Conventional Commits](https://www.conventionalcommits.org/)**:
   ```bash
   git commit -m "feat(component): add new feature"
   ```
5. **Push and create a Pull Request**
6. **Wait for review and address feedback**

### Important Guidelines

- ✅ **All changes must start in a separate branch**
- ✅ **Use Conventional Commits format** for all commit messages
- ✅ **Create a Pull Request** before merging to `main`
- ✅ **All tests must pass** before merge
- ✅ **Every merge to `main` must be tagged** with a version
- ✅ **Create a GitHub Release** for each version

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for complete details.

### Commit Message Format

```
<type>(<scope>): <subject>

Examples:
feat(csv-import): add support for custom delimiters
fix(notes): resolve duplicate tag issue
docs(readme): update installation instructions
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`

---

## Technology Stack

### Backend (Implemented through v0.5.0)
- **Python 3.10+** – Programming language
- **FastAPI** – Modern web framework
- **Uvicorn** – ASGI server used for local development
- **SQLAlchemy** – ORM for database connectivity
- **SQLite** – Local database for persistent storage

### Backend Features Delivered
- CSV import API with metadata persistence
- Notes API for creating and listing notes tied to CSV rows
- SQLite database connection with SQLAlchemy ORM and models for imports, rows, and notes
- Health and status endpoints exposed via FastAPI

### DevOps & Tooling
- **Docker** – Containerization
- **Docker Compose** – Service orchestration

### Frontend (Introduced in v0.4.0)
- **React 18** – Component framework
- **Vite** – Frontend tooling and dev server

### Planned Additions
- **pandas** – CSV processing and data manipulation
- **Ant Design** – Planned component library
- **Redux Toolkit** – Planned state management
- **pytest / Vitest** – Planned testing frameworks

---

## Project Status

### Current Version: 0.5.0 (In Development)

This project is under active development. The application is being built incrementally following the roadmap in [`development-plan.md`](development-plan.md).

### Development Progress

- [x] Version 0.1.0 - Hello World + Docker
- [x] Version 0.2.0 - Database Foundation
- [x] Version 0.3.0 - Basic CSV Import
- [x] Version 0.4.0 - Simple Data Display
- [x] Version 0.5.0 - Single Note Creation
- [ ] Version 0.6.0 - Note Display
- [ ] Version 0.7.0 - Note Editing
- [ ] Version 0.8.0 - Note Tags
- [ ] Version 0.9.0 - Primary Key Detection
- [ ] Version 1.0.0 - MVP Complete

See [`development-plan.md`](development-plan.md) for detailed milestones and timelines.

### Getting Updates

To stay informed about project progress:
- Watch this repository for updates
- Check [releases](../../releases) for new versions
- Review the [CHANGELOG](CHANGELOG.md) for version history

---

## Data Persistence

The application now ships with a SQLite database managed through SQLAlchemy. Database files are stored in the `data/` directory and persist across container restarts when using Docker Compose.

---

## API Documentation

Once the application is running, interactive API documentation is available at:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **OpenAPI JSON**: http://localhost:8080/openapi.json

---

## Troubleshooting

### Common Issues

**Port 8080 already in use**
```bash
# Check what's using the port
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Stop the application
docker-compose down
```

**Changes not reflected after code updates**
- Restart the container: `docker-compose restart`
- When running locally, stop Uvicorn (Ctrl+C) and restart the command

For more troubleshooting tips, see [`development-plan.md#troubleshooting-guide`](development-plan.md#troubleshooting-guide).

---

## Development Setup

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Git

### Local Development (without Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Running Tests

Tests are not yet available for version 0.1.0. Future releases will introduce automated test suites for both backend and frontend components.

---

## Roadmap

### Phase 1: MVP (Versions 0.1 - 1.0)
- Core CSV import and note management
- Basic UI with note display and editing
- Tag system and status management
- Docker deployment

### Phase 2: Enhanced Features (Versions 1.1 - 1.5)
- Orphaned row detection
- Advanced filtering and search
- Custom views
- Export functionality
- Production-ready polish

### Phase 3: Future Enhancements
- Multi-user support
- Real-time collaboration
- Advanced analytics
- API integrations
- Mobile responsive design

See [`csv-notes-spec.md`](csv-notes-spec.md) for the complete feature specification.

---

## Version Management

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

All version changes are documented in [CHANGELOG.md](CHANGELOG.md).

---

## Support

### Getting Help

- 📖 Read the [documentation](#documentation)
- 🐛 Report bugs via [GitHub Issues](../../issues)
- 💡 Request features via [GitHub Issues](../../issues)
- 💬 Ask questions in [GitHub Discussions](../../discussions)

### Reporting Issues

When reporting issues, please include:
- Version number
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Screenshots (if applicable)

---

## Security

### Reporting Security Issues

If you discover a security vulnerability, please email [security@example.com] instead of using the issue tracker.

### Current Security Model

- **Local-only access**: Services are intended to run on developer machines only.
- **Minimal surface area**: Version 0.1.0 exposes read-only informational endpoints.

Planned hardening work (database permissions, extended validation, etc.) is described in [`architecture.md#security-architecture`](architecture.md#security-architecture).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Ant Design](https://ant.design/) - Component library
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [pandas](https://pandas.pydata.org/) - Data processing

---

## Contact

- **Project Repository**: [GitHub](../../)
- **Documentation**: [Docs](../../wiki)
- **Issue Tracker**: [Issues](../../issues)

---

**Built with ❤️ for efficient CSV data management**
