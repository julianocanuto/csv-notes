# Contributing to CSV Notes Manager

Thank you for your interest in contributing to CSV Notes Manager! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Commit Message Convention](#commit-message-convention)
5. [Pull Request Process](#pull-request-process)
6. [Version Management](#version-management)
7. [Code Style Guidelines](#code-style-guidelines)
8. [Testing Requirements](#testing-requirements)

---

## Code of Conduct

This project adheres to professional standards of conduct. Be respectful, inclusive, and constructive in all interactions.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd csv-notes

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Run tests
cd ../backend && pytest
cd ../frontend && npm test
```

---

## Development Workflow

### Branching Strategy

**All changes MUST start in a separate branch.** Direct commits to `main` are not allowed.

#### Branch Naming Convention

```
<type>/<short-description>

Examples:
feature/csv-import-validation
fix/note-duplicate-tags
docs/update-api-documentation
refactor/database-queries
test/csv-processor-unit-tests
chore/update-dependencies
```

#### Branch Types

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks (dependencies, configs)
- `hotfix/` - Urgent production fixes

### Workflow Steps

1. **Create a new branch from `main`:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and commit using conventional commits** (see below)

3. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** (see Pull Request Process below)

5. **After review and approval, merge to `main`**

6. **Delete your feature branch after merge**

---

## Commit Message Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(csv-import): add auto-detection of primary key` |
| `fix` | Bug fix | `fix(notes): resolve duplicate tag creation issue` |
| `docs` | Documentation changes | `docs(readme): update installation instructions` |
| `style` | Code style changes (formatting, semicolons, etc.) | `style(backend): apply black formatter` |
| `refactor` | Code refactoring (no feature changes) | `refactor(database): optimize query performance` |
| `test` | Adding or updating tests | `test(csv-processor): add unit tests for validation` |
| `chore` | Build process or auxiliary tool changes | `chore(deps): update pandas to 2.1.3` |
| `perf` | Performance improvements | `perf(search): add index to notes table` |
| `ci` | CI/CD changes | `ci(github): add automated testing workflow` |
| `build` | Build system changes | `build(docker): update Dockerfile` |
| `revert` | Revert a previous commit | `revert: feat(csv-import): remove auto-detection` |

### Scope (Optional)

The scope identifies which part of the codebase is affected:

- `csv-import` - CSV import functionality
- `notes` - Note management
- `views` - View management
- `search` - Search and filter
- `export` - Export functionality
- `database` - Database models/schema
- `api` - API endpoints
- `ui` - User interface components
- `backend` - General backend changes
- `frontend` - General frontend changes
- `deps` - Dependencies
- `config` - Configuration files

### Subject

- Use imperative, present tense: "add" not "added" or "adds"
- Don't capitalize the first letter
- No period (.) at the end
- Limit to 72 characters

### Body (Optional)

- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Separate from subject with a blank line

### Footer (Optional)

- Reference issues: `Closes #123` or `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

#### Simple commit
```bash
git commit -m "feat(csv-import): add support for custom delimiters"
```

#### Commit with body
```bash
git commit -m "fix(notes): prevent duplicate tags on note creation

The tag creation logic was not checking for existing tags,
causing duplicates when users added the same tag multiple times.
Added validation to check existing tags before insertion.

Fixes #42"
```

#### Breaking change
```bash
git commit -m "feat(api): change note status enum values

BREAKING CHANGE: Note status values changed from 'open', 'closed'
to 'Open', 'In Progress', 'Resolved', 'Closed'. API consumers
must update their status filters accordingly.

Closes #78"
```

### Commit Message Validation

This project uses `commitlint` to validate commit messages. Install the git hook:

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
npx husky install
npx husky add .husky/commit-msg 'npx --no-install commitlint --edit "$1"'
```

---

## Pull Request Process

### Before Creating a PR

1. **Ensure all tests pass:**
   ```bash
   # Backend tests
   cd backend && pytest
   
   # Frontend tests
   cd frontend && npm test
   ```

2. **Update documentation** if needed:
   - Update README.md for user-facing changes
   - Update API documentation for endpoint changes
   - Update architecture.md for architectural changes

3. **Update CHANGELOG.md** with your changes under "Unreleased" section

4. **Lint your code:**
   ```bash
   # Backend
   cd backend && black . && flake8
   
   # Frontend
   cd frontend && npm run lint
   ```

### Creating a Pull Request

1. **Push your branch** to the repository
2. **Create a PR** from your branch to `main`
3. **Fill out the PR template** completely (see `.github/pull_request_template.md`)
4. **Link related issues** using keywords (Closes #123)
5. **Request review** from relevant team members

### PR Title Format

Use the same conventional commit format:

```
<type>(<scope>): <description>

Examples:
feat(csv-import): add support for Excel files
fix(notes): resolve tag sorting issue
docs(contributing): add branching strategy guidelines
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Closes #<issue_number>

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests passing
```

### Review Process

1. **At least one approval required** before merging
2. **All checks must pass** (tests, linting, etc.)
3. **Address review comments** promptly
4. **Resolve all conversations** before merging
5. **Squash commits** if multiple small commits exist (optional)

### After PR Approval

1. **Merge to main** (use "Squash and merge" or "Merge commit")
2. **Delete the feature branch**
3. **Verify the deployment** (if applicable)

---

## Version Management

### Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

Example: 1.2.3
```

- **MAJOR** (1.x.x): Breaking changes, incompatible API changes
- **MINOR** (x.2.x): New features, backwards-compatible
- **PATCH** (x.x.3): Bug fixes, backwards-compatible

### Creating a Release

**All versions merged to `main` MUST have a tag and a new release.**

#### Steps:

1. **Update version numbers:**
   ```bash
   # Backend version
   # Update version in backend/app/config.py or __init__.py
   
   # Frontend version
   # Update version in frontend/package.json
   ```

2. **Update CHANGELOG.md:**
   - Move "Unreleased" changes to new version section
   - Add date of release
   - Follow [Keep a Changelog](https://keepachangelog.com/) format

3. **Update README.md** (if needed):
   - Update version badges
   - Update installation instructions
   - Update feature list for major versions
   - Update compatibility information

4. **Commit version changes:**
   ```bash
   git add .
   git commit -m "chore(release): bump version to 1.2.0"
   git push origin main
   ```

5. **Create and push tag:**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

6. **Create GitHub Release:**
   - Go to GitHub repository → Releases → "Create a new release"
   - Select the tag (v1.2.0)
   - Release title: `Version 1.2.0`
   - Description: Copy from CHANGELOG.md for this version
   - Attach build artifacts (if applicable)
   - Mark as pre-release if beta/alpha
   - Publish release

### CHANGELOG.md Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features go here

### Changed
- Changes to existing features

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes

## [1.2.0] - 2025-11-04

### Added
- CSV import with custom delimiters
- Export to Excel format

### Fixed
- Duplicate tag creation issue
- Search performance on large datasets

## [1.1.0] - 2025-10-15
...
```

---

## Code Style Guidelines

### Python (Backend)

- **Formatter**: [Black](https://black.readthedocs.io/) (line length: 88)
- **Linter**: [Flake8](https://flake8.pycqa.org/)
- **Type Hints**: Use Python type hints for all functions
- **Docstrings**: Use Google-style docstrings

```python
def process_csv_import(file_path: str, primary_key: str) -> Dict[str, Any]:
    """
    Process CSV file import and update database.
    
    Args:
        file_path: Path to CSV file
        primary_key: Name of primary key column
        
    Returns:
        Dictionary with import statistics
        
    Raises:
        ValidationError: If CSV format is invalid
    """
    pass
```

### JavaScript/React (Frontend)

- **Formatter**: [Prettier](https://prettier.io/)
- **Linter**: [ESLint](https://eslint.org/)
- **Style**: Use functional components with hooks
- **Naming**: PascalCase for components, camelCase for functions

```javascript
/**
 * DataTable component displays CSV data with expandable rows.
 * 
 * @param {Object} props - Component props
 * @param {Array} props.data - Array of row objects
 * @param {Function} props.onRowExpand - Callback when row is expanded
 * @returns {JSX.Element} Rendered table component
 */
const DataTable = ({ data, onRowExpand }) => {
  // Component implementation
};
```

### File Naming

- **Python**: `snake_case.py` (e.g., `csv_processor.py`)
- **JavaScript**: `PascalCase.jsx` for components, `camelCase.js` for utilities
- **Tests**: `test_*.py` or `*.test.js`

---

## Testing Requirements

### Backend Testing (pytest)

```bash
cd backend
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest --cov=app                 # With coverage
pytest tests/test_csv.py         # Specific test file
```

**Requirements:**
- Unit tests for all business logic
- Integration tests for API endpoints
- Minimum 80% code coverage
- All tests must pass before PR merge

### Frontend Testing (Vitest/Jest)

```bash
cd frontend
npm test                         # Run all tests
npm run test:coverage            # With coverage
npm run test:watch               # Watch mode
```

**Requirements:**
- Component tests using React Testing Library
- Unit tests for utility functions
- Integration tests for critical user flows
- Minimum 70% code coverage

### Writing Tests

**Python Example:**
```python
def test_detect_primary_key_column():
    """Test primary key auto-detection."""
    df = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['A', 'B', 'C']})
    result = CSVProcessor.detect_primary_key_column(df)
    assert result == 'ID'
```

**JavaScript Example:**
```javascript
test('renders note list correctly', () => {
  const notes = [{ note_id: 1, note_text: 'Test note' }];
  render(<NotesList notes={notes} />);
  expect(screen.getByText('Test note')).toBeInTheDocument();
});
```

---

## Additional Guidelines

### Documentation

- Update documentation alongside code changes
- Use clear, concise language
- Include examples where helpful
- Keep documentation in sync with code

### Code Review Checklist

Before requesting review, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] Code is self-documented or has comments for complex logic
- [ ] No commented-out code or debug statements
- [ ] No hardcoded values (use configuration)
- [ ] Error handling is appropriate
- [ ] Logging is added for important operations
- [ ] Documentation is updated
- [ ] Commit messages follow conventional commits
- [ ] CHANGELOG.md is updated

### Getting Help

- Check existing documentation first
- Search closed issues for similar problems
- Ask questions in discussions or issues
- Be specific about your environment and problem

---

## Release Schedule

- **Patch releases**: As needed for bug fixes
- **Minor releases**: Monthly (if features are ready)
- **Major releases**: Quarterly or as needed for breaking changes

---

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

Thank you for contributing to CSV Notes Manager! 🎉