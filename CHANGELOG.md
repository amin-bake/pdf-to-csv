# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-12

### Added

- Initial release of PDF to CSV converter
- Multiple file upload support with drag & drop interface
- Real-time upload and conversion progress tracking
- Automatic table extraction using pdfplumber
- Alternative Tabula parser support for complex table layouts
- Automatic table merging per PDF file
- Individual file download buttons
- "Download All" button to download all files as a single ZIP
- Background processing with threading
- Status polling for conversion progress
- Per-file error handling and reporting
- Responsive UI that works on desktop and mobile
- Smart download behavior (CSV for single files, ZIP for multiple)
- Flask-based REST API backend
- Comprehensive test suite

### Features

- **Upload**: XHR-based upload with progress events
- **Conversion**: Background processing with status updates
- **Download**: Blob-based downloads without page reload
- **UI**: Clean, intuitive interface with visual feedback
- **Parser Options**: Choose between pdfplumber and Tabula
- **Batch Processing**: Handle multiple PDFs simultaneously
- **Fallback**: Extract text content if no tables found

### Documentation

- README with installation and usage instructions
- Contributing guidelines (CONTRIBUTING.md)
- Deployment guide with security recommendations (DEPLOYMENT.md)
- Security policy (SECURITY.md)
- MIT License
- Comprehensive test suite

### Technical Details

- Flask 2.x+ web framework
- pdfplumber for PDF parsing
- pandas for CSV generation
- In-memory file storage with UUID-based IDs
- Temporary file system storage
- Content-Disposition headers for proper filenames
- ZIP compression for batch downloads

## [Unreleased]

### Planned Features

- Docker containerization
- Cloud storage integration (S3, Azure Blob, GCS)
- Persistent database for file metadata
- Authentication and authorization
- Rate limiting
- Advanced table detection options
- Support for additional output formats (Excel, JSON)
- Scheduled file cleanup
- API documentation (Swagger/OpenAPI)
- Automated testing in CI/CD pipeline

---

[1.0.0]: https://github.com/YOUR_USERNAME/pdf-to-csv/releases/tag/v1.0.0
