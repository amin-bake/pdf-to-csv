# Project Structure

This document outlines the structure and organization of the PDF to CSV converter project.

## Directory Structure

```
pdf-to-csv/
│
├── .github/                          # GitHub-specific files
│   ├── ISSUE_TEMPLATE/              # Issue templates
│   │   ├── bug_report.md           # Bug report template
│   │   ├── feature_request.md      # Feature request template
│   │   └── question.md             # Question template
│   ├── workflows/                   # GitHub Actions workflows
│   │   ├── tests.yml               # Automated testing workflow
│   │   └── security.yml            # Security audit workflow
│   └── pull_request_template.md    # Pull request template
│
├── templates/                        # HTML templates
│   └── index.html                   # Main web interface
│
├── app.py                           # Flask application (main backend)
├── wsgi.py                          # WSGI entry point for production
├── requirements.txt                 # Python dependencies
│
├── test_e2e.py                      # End-to-end integration tests
├── test_upload.py                   # Upload functionality tests
├── test_download_types.py           # Download behavior tests
├── test_download_all.py             # Batch download tests
│
├── README.md                        # Project overview and setup
├── CONTRIBUTING.md                  # Contribution guidelines
├── CODE_OF_CONDUCT.md              # Code of conduct
├── DEPLOYMENT.md                    # Production deployment guide
├── SECURITY.md                      # Security policy
├── CHANGELOG.md                     # Version history and changes
├── TESTS.md                         # Test documentation
├── LICENSE                          # MIT License
├── .gitignore                       # Git ignore patterns
└── INSTRUCTIONS.md                  # Original project instructions

```

## File Descriptions

### Core Application Files

#### `app.py`

The main Flask application containing:

- **Routes**: `/`, `/upload`, `/convert`, `/status/<id>`, `/download/<id>`, `/download_all`
- **Conversion Logic**: PDF parsing using pdfplumber and tabula
- **File Management**: Temporary file storage and metadata tracking
- **Background Processing**: Threading for non-blocking conversions

**Key Functions:**

- `_save_uploaded_file_storage()` - Saves uploaded files to temp storage
- `tables_from_pdf_bytes()` - Extracts tables using pdfplumber
- `convert_file()` - Background conversion worker
- `start_conversion_background()` - Starts conversion threads

#### `wsgi.py`

Production WSGI entry point for deployment with Gunicorn, Waitress, or uWSGI.

#### `templates/index.html`

Single-page application containing:

- **Upload UI**: Drag-and-drop file upload with progress
- **Conversion Controls**: Parser selection and convert button
- **Progress Tracking**: Real-time status updates
- **Download Interface**: Individual and batch download buttons
- **JavaScript Logic**: XHR uploads, fetch downloads, polling

### Configuration Files

#### `requirements.txt`

Python package dependencies:

- `Flask>=2.0` - Web framework
- `pdfplumber>=0.7` - PDF parsing
- `pandas>=1.0` - Data manipulation
- `tabula-py>=2.0` - Alternative parser
- `requests>=2.28` - HTTP library for tests

#### `.gitignore`

Excludes from version control:

- Python bytecode and caches
- Virtual environments
- Temporary files
- IDE configurations
- Generated PDFs/CSVs/ZIPs

### Documentation Files

#### `README.md`

- Project overview
- Features list
- Installation instructions
- Usage guide
- Architecture overview
- API documentation
- Contributing information

#### `CONTRIBUTING.md`

- How to contribute
- Development setup
- Code style guidelines
- Commit message conventions
- Pull request process

#### `DEPLOYMENT.md`

- Security considerations
- Production server setup options
- Docker configuration
- File storage recommendations
- Monitoring and logging
- Environment variables
- Production checklist

#### `SECURITY.md`

- Security policy
- Vulnerability reporting process
- Known security limitations
- Best practices
- Dependency security

#### `CHANGELOG.md`

- Version history
- Feature additions
- Bug fixes
- Breaking changes
- Future roadmap

#### `TESTS.md`

- Test suite overview
- Individual test descriptions
- Running instructions
- Adding new tests
- CI/CD integration

#### `CODE_OF_CONDUCT.md`

- Community standards
- Enforcement guidelines
- Attribution to Contributor Covenant

### Test Files

All tests are standalone Python scripts that:

- Connect to running Flask server
- Perform operations via HTTP API
- Verify responses and content
- Print progress and results
- Exit with status code

#### `test_e2e.py`

Full workflow test: upload → convert → status → download

#### `test_upload.py`

Upload endpoint validation and file handling

#### `test_download_types.py`

CSV vs ZIP download logic verification

#### `test_download_all.py`

Batch download functionality test

### GitHub Templates

#### Issue Templates

- `bug_report.md` - Structured bug reports
- `feature_request.md` - Feature suggestions
- `question.md` - General questions

#### Pull Request Template

- Change description
- Testing checklist
- Documentation updates
- Code review guidelines

### GitHub Actions Workflows

#### `tests.yml`

- Runs on push and PR
- Matrix testing (multiple OS and Python versions)
- Automated test execution

#### `security.yml`

- Weekly security audits
- Dependency vulnerability scanning
- pip-audit and safety checks

## Data Flow

```
User Browser
    ↓ (Upload PDFs)
Flask /upload endpoint
    ↓ (Save to temp storage)
In-memory uploaded_files dict
    ↓ (User clicks Convert)
Flask /convert endpoint
    ↓ (Start background threads)
convert_file() function
    ↓ (Extract tables)
pdfplumber / tabula
    ↓ (Write CSVs)
Temporary files on disk
    ↓ (User clicks Download)
Flask /download or /download_all
    ↓ (Send file/ZIP)
User Browser (downloads file)
```

## State Management

### In-Memory Storage

```python
uploaded_files = {
    'file_id': {
        'id': 'uuid',
        'name': 'filename.pdf',
        'path': '/tmp/path.pdf',
        'status': 'uploaded|converting|done|error',
        'progress': 0-100,
        'converted_files': ['/tmp/file.csv'],
        'error': None or 'error message'
    }
}
```

### File System

- Uploaded PDFs: `tempfile.mkstemp()` in system temp
- Converted CSVs: `tempfile.mkdtemp()` directories per file
- Downloaded ZIPs: Generated in-memory with `io.BytesIO()`

## API Endpoints

| Method | Endpoint         | Purpose            | Request                     | Response                                               |
| ------ | ---------------- | ------------------ | --------------------------- | ------------------------------------------------------ |
| GET    | `/`              | Web UI             | -                           | HTML                                                   |
| POST   | `/upload`        | Single file upload | FormData with file          | `{id, name}`                                           |
| POST   | `/convert`       | Start conversion   | `{file_ids, parser, merge}` | `{started, file_ids}`                                  |
| GET    | `/status/<id>`   | Poll status        | -                           | `{id, name, status, progress, converted_files, error}` |
| GET    | `/download/<id>` | Download file      | -                           | CSV or ZIP file                                        |
| POST   | `/download_all`  | Download all       | `{file_ids}`                | ZIP file                                               |

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.x
- **PDF Processing**: pdfplumber, tabula-py
- **Data Handling**: pandas
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **File I/O**: tempfile, zipfile, io
- **Concurrency**: threading
- **Testing**: requests library
- **CI/CD**: GitHub Actions

## Extension Points

Areas designed for customization:

1. **Parser Selection**: Add new PDF parsers in `convert_file()`
2. **Storage Backend**: Replace tempfile with cloud storage
3. **Authentication**: Add auth middleware to routes
4. **Rate Limiting**: Implement with Flask-Limiter
5. **Output Formats**: Add Excel, JSON exporters
6. **Cleanup**: Implement scheduled file deletion
7. **Monitoring**: Add logging and metrics
8. **Database**: Replace in-memory dict with persistent storage

## Dependencies

### Direct Dependencies

- Flask - Web framework
- pdfplumber - PDF parsing (pdfminer.six backend)
- pandas - CSV generation
- tabula-py - Alternative parser (requires Java)
- requests - Testing only

### Transitive Dependencies

See `pip list` for complete dependency tree including:

- Werkzeug (Flask dependency)
- Jinja2 (Flask templates)
- pdfminer.six (pdfplumber backend)
- Pillow (image processing)
- numpy (pandas dependency)

## Maintenance Notes

### Regular Tasks

- Update dependencies: `pip install -U -r requirements.txt`
- Run security audits: `pip-audit`
- Test across Python versions
- Review and respond to issues
- Merge dependabot PRs

### Before Release

- Run all tests
- Update CHANGELOG.md
- Create GitHub release
- Tag version in git
- Update badges in README

---

For more information, see individual documentation files.
