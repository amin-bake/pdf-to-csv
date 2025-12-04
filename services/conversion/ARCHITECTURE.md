# Conversion Service Architecture

## Overview

The conversion service has been refactored from a monolithic 1180-line file into a modular, layered architecture following best practices for scalability, maintainability, and reduced coupling.

## Architecture Layers

### 1. **Extraction Layer** (`extractors.py`)

**Purpose**: Pure PDF data extraction with no business logic

**Functions**:

- `extract_tables_pdfplumber(pdf_path)`: Extracts tables from PDF using pdfplumber
- `extract_text_lines(pdf_path)`: Fallback text extraction for non-tabular documents
- `extract_structured_text_json(pdf_path)`: Structured text extraction for CVs/resumes with page organization

**Dependencies**: Only pdfplumber
**Lines of Code**: 84

### 2. **Analysis Layer** (`analyzers.py`)

**Purpose**: Table intelligence and structure analysis

**Functions**:

- `clean_header(header)`: Normalizes header text (removes newlines, extra whitespace)
- `is_title_row(row)`: Detects title rows (≤2 cells, long text)
- `analyze_table_structure(table)`: Multi-dimensional row classification
  - Scoring system: +5 for header keywords, -10 for barcodes, -8 for currency
  - Returns: title_rows, header_row_idx, data_start_idx, column_count, has_sequential_ids
- `create_headers(row, col_count, structure)`: Intelligent column naming (sequential IDs → "id", fallback → "column_X")
- `validate_table_data(tables)`: Validates 70% multi-column threshold

**Dependencies**: No external module imports
**Lines of Code**: 272

### 3. **Conversion Layer** (`converters.py`)

**Purpose**: Format-specific output file generation

**Functions**:

- `save_tables_to_csv(tables, output_dir, base_filename, merge)`: CSV generation with merge support
- `save_tables_to_excel(tables, output_dir, base_filename, merge)`: Excel with auto-adjusted column widths
- `save_tables_to_json(tables, output_dir, base_filename, merge, pdf_path)`: Intelligent JSON conversion
  - Uses `validate_table_data()` to detect CVs
  - Implements master header strategy for merge mode
  - Falls back to `extract_structured_text_json()` for text documents
  - Handles duplicate header detection across tables

**Dependencies**: Imports from analyzers and extractors
**Lines of Code**: 350

### 4. **Orchestration Layer** (`worker.py`)

**Purpose**: Background job orchestration and threading

**Classes**:

- `ConversionWorker`: Main orchestrator class

**Methods**:

- `__init__(upload_folder, converted_folder, conversion_jobs)`: Initializes worker with configuration
- `start_conversion(file_ids, parser, merge, output_format)`: Creates job and starts background thread
- `process_conversion(job_id, file_infos, parser, merge, output_format)`: Background conversion workflow
- `_find_pdf_file(file_id)`: Locates files by ID in upload folder
- `_extract_tables(pdf_path, parser)`: Parser selection (pdfplumber vs tabula)
- `_convert_to_format(tables, file_output_dir, base_filename, merge, output_format, pdf_path)`: Routes to appropriate converter

**Dependencies**: Imports from extractors and converters
**Lines of Code**: 178

### 5. **API Layer** (`app.py`)

**Purpose**: Flask HTTP endpoints and initialization

**Routes**:

- `GET /api/health`: Health check endpoint
- `POST /api/convert`: Start conversion job
- `GET /api/status/<job_id>`: Check job status

**Configuration**:

- Initializes Flask app and CORS
- Sets up upload and conversion folders
- Instantiates ConversionWorker

**Dependencies**: Imports from worker module
**Lines of Code**: 128 (reduced from 1180+)

## Design Principles

### Single Responsibility Principle

Each module has one clear purpose:

- Extractors extract data
- Analyzers analyze structure
- Converters generate output files
- Worker orchestrates jobs
- App handles HTTP requests

### Separation of Concerns

- **Data layer** is isolated from business logic
- **Intelligence layer** doesn't know about file formats
- **Conversion layer** uses analyzers without knowing extraction details
- **Orchestration layer** coordinates without implementing logic
- **API layer** handles HTTP without conversion details

### Reduced Coupling

- Clear interfaces between layers
- Minimal cross-module dependencies
- Each module can be tested independently

### Improved Testability

- Can mock extractors to test analyzers
- Can test converters with sample data
- Can test worker without running Flask app

### Better Maintainability

- Changes isolated to specific modules
- Easy to add new parsers (just modify extractors)
- Easy to add new formats (just add to converters)
- Easy to change intelligence (just modify analyzers)

### Scalability Benefits

- Can run workers on separate processes/servers
- Can swap implementations without touching other layers
- Can add caching at any layer
- Errors don't cascade through entire system

## Data Flow

```
1. HTTP Request → app.py
2. app.py → worker.start_conversion()
3. worker → extractors.extract_tables_pdfplumber()
4. worker → converters.save_tables_to_*()
5. converters → analyzers.analyze_table_structure()
6. converters → extractors.extract_structured_text_json() (fallback)
7. worker updates job status
8. app.py returns job status on request
```

## Module Dependency Graph

```
app.py
  └─→ worker.py
       ├─→ extractors.py (pure extraction)
       └─→ converters.py
            ├─→ analyzers.py (intelligence)
            └─→ extractors.py (for text fallback)
```

## Benefits Over Monolithic Design

### Before (Monolithic)

- 1180 lines in one file
- All logic mixed together
- Hard to test
- Difficult to modify safely
- Tightly coupled
- Single point of failure

### After (Modular)

- 5 focused modules (128 + 178 + 84 + 272 + 350 = 1012 lines)
- Clear separation of concerns
- Easy to test components independently
- Safe to modify individual modules
- Loosely coupled with clear interfaces
- Fault isolation

## Future Enhancements

### Easy to Add

1. **New Parser**: Add to extractors.py, update worker.\_extract_tables()
2. **New Format**: Add converter function to converters.py, update worker.\_convert_to_format()
3. **New Intelligence**: Add to analyzers.py, use in converters
4. **Caching**: Add caching layer in worker or converters
5. **Queue System**: Replace threading with Celery/RQ in worker
6. **Monitoring**: Add logging/metrics in worker without touching other modules

### Testing Strategy

1. **Unit Tests**:

   - Test each analyzer function with sample tables
   - Test each converter with mock data
   - Test each extractor with sample PDFs

2. **Integration Tests**:

   - Test worker with mock extractors/converters
   - Test full flow with sample PDFs

3. **End-to-End Tests**:
   - Test API endpoints with real PDFs
   - Verify all output formats

## Migration Notes

### Breaking Changes

None - API endpoints remain unchanged

### Configuration

No changes required - same environment variables and folder structure

### Dependencies

All dependencies remain the same (Flask, pdfplumber, openpyxl, pandas)

### Deployment

No changes required - same entry point (app.py)
