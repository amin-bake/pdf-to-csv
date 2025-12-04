# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed - 2025-12-04

#### 🎨 Frontend Refactoring: Reusable Conversion Components

Refactored all conversion pages (CSV, Excel, JSON, Text) to eliminate code duplication by creating reusable components and custom hooks.

**Code Improvements:**

- **Reduced Duplication**: Eliminated ~950 lines of duplicated code across 4 pages
- **Page Simplification**: Each conversion page reduced from ~390 lines to ~22 lines (94% reduction)
- **Shared Architecture**: Created centralized conversion logic and UI components
- **Type Safety**: Enhanced type safety with centralized configuration system

**New Components:**

- **ConversionPageLayout**: Reusable UI layout component for all conversion pages (~200 lines)
- **useConversionPage Hook**: Custom hook encapsulating all conversion logic (~280 lines)
- **conversionConfig**: Centralized format configurations with type-safe definitions (~45 lines)

**Refactored Pages:**

- `frontend/app/convert/pdf-to-csv/page.tsx`: 390 lines → 22 lines
- `frontend/app/convert/pdf-to-excel/page.tsx`: 390 lines → 22 lines
- `frontend/app/convert/pdf-to-json/page.tsx`: 386 lines → 22 lines
- `frontend/app/convert/pdf-to-text/page.tsx`: 386 lines → 22 lines

**Benefits:**

- **Maintainability**: Bug fixes and feature updates now apply to all formats automatically
- **Scalability**: Adding new conversion format takes ~5 minutes (was 30+ minutes)
- **Consistency**: Guaranteed identical behavior across all conversion types
- **DRY Principle**: Single source of truth for conversion page logic
- **Developer Experience**: Clear component responsibilities and self-documenting through types

**Technical Details:**

- Created `OutputFormat` type union for type-safe format handling
- Implemented centralized configuration system with `ConversionConfig` interface
- Extracted all state management, handlers, and UI into reusable components
- Maintained full backwards compatibility (zero breaking changes)
- Preserved all existing functionality and user experience

**Documentation:**

- Created `FRONTEND_REFACTORING.md` with comprehensive refactoring details
- Documented architecture, design decisions, and usage examples
- Included metrics showing 61% overall code reduction

### Added - 2025-12-04

#### 📄 PDF to Text Conversion

Added new PDF to plain text conversion format with intelligent table formatting and full text extraction.

**Features:**

- **Text Format Support**: New `save_tables_to_text()` converter function in `converters.py`
- **Intelligent Detection**: Automatically detects whether document contains tables or plain text
- **Table Formatting**: For tabular documents, formats tables with aligned columns for readability
- **Full Text Extraction**: For text documents (CVs, resumes, reports), extracts complete text with page separators
- **Merge Support**: Can merge multiple tables/pages into single text file or keep separate
- **Frontend Page**: New `/convert/pdf-to-text` page with full UI integration
- **API Support**: Backend updated to handle `outputFormat: "text"` parameter

**Technical Implementation:**

- Added `save_tables_to_text()` function to `converters.py` (uses `validate_table_data()` for detection)
- Updated `worker._convert_to_format()` to route 'text' format to new converter
- Added pdfplumber import to `converters.py` for direct text extraction
- Updated API documentation in `app.py` to include text format
- Created `frontend/app/convert/pdf-to-text/page.tsx` with complete conversion workflow

**User Benefits:**

- Clean, readable plain text output
- Preserves document structure and formatting
- Perfect for text analysis, NLP applications, and content extraction
- Column-aligned tables for better readability in text format

**Documentation:**

- Updated `README.md` with PDF to Text conversion details
- Added text format to usage instructions and features list
- Homepage updated with PDF to Text conversion option (enabled)

### Changed - 2025-12-03

#### 🏗️ Conversion Service Refactoring: Modular Architecture

Refactored the conversion service from a monolithic 1180-line file into a clean, modular architecture following industry best practices.

**Architecture Improvements:**

- **Modular Design**: Separated into 5 focused modules (128 + 178 + 84 + 272 + 350 lines)
  - `app.py` (128 lines) - API Layer: Flask routes only
  - `worker.py` (178 lines) - Orchestration Layer: Background job management
  - `extractors.py` (84 lines) - Extraction Layer: Pure PDF data extraction
  - `analyzers.py` (272 lines) - Analysis Layer: Table intelligence & structure detection
  - `converters.py` (350 lines) - Conversion Layer: Format-specific output generation
- **Separation of Concerns**: Each layer has a single, clear responsibility
- **Improved Testability**: Components can be tested independently with mocking
- **Better Maintainability**: Changes isolated to specific modules (70% smaller files)
- **Enhanced Scalability**: Easy to add new parsers or formats without touching other code
- **Reduced Coupling**: Clear interfaces between layers with minimal dependencies
- **Fault Isolation**: Errors contained within specific modules for easier debugging

**Technical Details:**

- Created layered architecture: API → Orchestration → Extraction/Analysis → Conversion
- Implemented clear data flow: HTTP Request → Worker → Extractors → Converters → Analyzers
- Module dependency graph ensures one-way dependencies (no circular references)
- Zero breaking changes to API endpoints (`/api/convert`, `/api/status/<job_id>`, `/api/health`)

**Bug Fixes:**

- Fixed `datetime.utcnow()` deprecation warnings (replaced with `datetime.now(timezone.utc)`)
- Fixed TypeError when passing `file_ids` list as `job_id` parameter
- Fixed Thread object JSON serialization error (now returns `job_id` string)
- Removed development print statements (`[INFO]` logs)

**Documentation:**

- Added `services/conversion/ARCHITECTURE.md` with comprehensive architecture documentation
- Updated root `README.md` with refactoring details and new module structure
- Created detailed PR description with metrics, diagrams, and testing strategy

**Benefits:**

- 14% reduction in total lines with cleaner, more focused code
- 70% reduction in largest module size (1180 → 350 lines)
- 400% increase in modularity (1 file → 5 modules)
- Enabled independent testing of each layer
- Reduced blast radius for code changes
- Easier onboarding for new developers

See `services/conversion/ARCHITECTURE.md` for detailed documentation.

## [Released]

### Added

- **PDF to JSON Conversion**: New conversion format for structured data export
  - Extract tables from PDFs to JSON format
  - Converts table rows to JSON objects with headers as keys
  - Supports both merged (single file) and separate file outputs
  - Dedicated `/convert/pdf-to-json` page with full UI
  - Backend support with proper MIME type handling
- **PDF to Excel Conversion**: New conversion format supporting Excel (.xlsx) output
  - Extract tables from PDFs to Excel spreadsheets
  - Multi-sheet support when merging tables
  - Auto-adjusted column widths for better readability
  - Dedicated `/convert/pdf-to-excel` page with full UI
  - Backend support with openpyxl library
- **Multi-Theme Color System**: Users can now switch between three beautiful color themes
  - 🌲 Earthy Forest (default) - Calm greens and earth tones
  - 🌸 Cherry Blossom Bloom - Vibrant reds and soft pinks
  - 🌈 Pastel Rainbow Fantasy - Dreamy pastels and rainbow hues
- **Color Theme Selector Component**: Palette icon dropdown for easy theme switching
- **Theme Persistence**: Selected theme saved to localStorage
- **Full Dark Mode Support**: Each color theme has optimized light and dark variants (6 total combinations)
- **Smooth Theme Transitions**: 0.3s ease transitions for professional feel
- **Dynamic Background Gradients**: Animated backgrounds adapt to selected theme
- **Comprehensive Theme Documentation**: Added `docs/COLOR_THEMES.md` with full implementation guide

### Changed

- Updated conversion service to support multiple output formats (CSV, Excel, and JSON)
- Enhanced API to accept `outputFormat` parameter in conversion requests (csv/excel/json)
- Enhanced download service to use correct MIME types for all formats
- Updated all hardcoded color values to use theme-aware CSS custom properties
- Refactored background gradients in layout to use dynamic CSS variables
- Enhanced global CSS with 27 new color families (243 color shades total)
- Updated homepage hero, cards, and feature icons to respect active theme

## [0.1.0] - 2025-12-02

### 🎉 Microservices Architecture Implementation

Migrated application from monolithic Flask to modern microservices architecture with Next.js frontend.

### Added

#### Frontend (Next.js 15 + TypeScript)

- **Modern UI Framework**: Next.js 15 with App Router and TypeScript 5
- **Styling**: Tailwind CSS v4 with custom design system
- **Dark Mode**: Full dark mode support with system detection and theme toggle
- **Component Library**: shadcn/ui components with Radix UI primitives
- **State Management**: Zustand for global state, React Query for server state
- **File Upload**: Enhanced drag-and-drop with real-time progress tracking
- **Status Tracking**: Visual file cards with status badges (uploading, uploaded, converting, completed, error)
- **Responsive Design**: Mobile-first design that works on all devices

#### Backend Microservices

- **Upload Service (Port 5001)**:

  - File upload with validation (PDF, 50MB max)
  - UUID-based file identification
  - Health check endpoint
  - CORS support for frontend integration

- **Conversion Service (Port 5002)**:

  - PDF to CSV conversion with pdfplumber
  - Background job processing with threading
  - Real-time progress tracking
  - Table extraction with merge support
  - Fallback to text extraction
  - Job status polling API

- **Download Service (Port 5003)**:
  - Single file download
  - Batch download as ZIP with original filenames preserved
  - File metadata endpoints
  - Cleanup operations

#### Infrastructure

- **Docker Compose**: Full development environment setup
- **Shared Libraries**: Common utilities and storage abstraction
- **Environment Configuration**: Service-specific environment variables
- **Health Checks**: All services expose health endpoints

### Changed

#### Architecture

- **Microservices Pattern**: Separated concerns into independent services
- **API Communication**: RESTful APIs with CORS support
- **File Storage**: Shared temporary storage with job-based organization
- **Progress Tracking**: Polling-based status updates (WebSocket support planned)

#### User Experience

- **Smart Downloads**: Single file downloads as CSV, multiple files as ZIP
- **Original Filenames**: Preserved in ZIP archives
- **Real-time Feedback**: Visual progress bars and status indicators
- **Error Handling**: Per-file error tracking and display
- **Theme Support**: Light, dark, and system theme options

#### Development

- **TypeScript**: Full type safety across frontend
- **Modern React**: Hooks, async operations, and optimistic updates
- **API Client**: Centralized API communication layer
- **Custom Hooks**: Reusable logic for upload, conversion, and download

### Fixed

- File status updates now properly track from upload through conversion
- Download functionality correctly routes to Download Service (was trying port 5000)
- Individual file downloads now work alongside batch downloads
- ZIP archives preserve original filenames (was using file IDs)
- Theme toggle icon properly changes color on hover

### Technical Details

#### Frontend Stack

- Next.js 15.5.6 with App Router
- React 19 with TypeScript 5
- Tailwind CSS v4
- shadcn/ui + Radix UI
- Zustand + React Query
- Lucide React icons

#### Backend Stack

- Flask 3.0.0
- pdfplumber 0.11.8 for PDF parsing
- Python 3.11+
- In-memory job tracking
- Temporary file system storage

#### Deployment

- Frontend: Ready for Vercel deployment
- Services: Containerized with Docker
- Local development: npm run dev (starts all services)
- Production: docker-compose with environment-specific configs

### Migration Status

- ✅ **Phase 1**: Project restructuring and documentation
- ✅ **Phase 2**: Frontend development with Next.js 15 + dark mode
- ✅ **Phase 3**: Backend microservices (Upload, Conversion, Download)
- 📋 **Phase 4**: Storage & Infrastructure improvements (S3, Redis)
- 📋 **Phase 5**: Testing & Documentation
- 📋 **Phase 6**: Production deployment & monitoring

### Breaking Changes

- **API Endpoints**: New service-specific URLs (5001, 5002, 5003)
- **Environment Variables**: New `NEXT_PUBLIC_*_SERVICE_URL` variables required
- **File IDs**: Now use UUIDs instead of timestamp-based IDs
- **Response Format**: Updated JSON structure for consistency

### Deprecated

- ❌ Legacy monolithic Flask app (moved to `/legacy` folder)
- ❌ Old API at port 5000
- ❌ In-app UI from Flask templates (replaced with Next.js)

---

## [0.0.1] - 2025-11-12

### Added

## [0.1.0] - 2025-12-02

### 🎉 Microservices Architecture Implementation

Migrated application from monolithic Flask to modern microservices architecture with Next.js frontend.

### Added

#### Frontend (Next.js 15 + TypeScript)

- **Modern UI Framework**: Next.js 15 with App Router and TypeScript 5
- **Styling**: Tailwind CSS v4 with custom design system
- **Dark Mode**: Full dark mode support with system detection and theme toggle
- **Component Library**: shadcn/ui components with Radix UI primitives
- **State Management**: Zustand for global state, React Query for server state
- **File Upload**: Enhanced drag-and-drop with real-time progress tracking
- **Status Tracking**: Visual file cards with status badges (uploading, uploaded, converting, completed, error)
- **Responsive Design**: Mobile-first design that works on all devices

#### Backend Microservices

- **Upload Service (Port 5001)**:

  - File upload with validation (PDF, 50MB max)
  - UUID-based file identification
  - Health check endpoint
  - CORS support for frontend integration

- **Conversion Service (Port 5002)**:

  - PDF to CSV conversion with pdfplumber
  - Background job processing with threading
  - Real-time progress tracking
  - Table extraction with merge support
  - Fallback to text extraction
  - Job status polling API

- **Download Service (Port 5003)**:
  - Single file download
  - Batch download as ZIP with original filenames preserved
  - File metadata endpoints
  - Cleanup operations

#### Infrastructure

- **Docker Compose**: Full development environment setup
- **Shared Libraries**: Common utilities and storage abstraction
- **Environment Configuration**: Service-specific environment variables
- **Health Checks**: All services expose health endpoints

### Changed

#### Architecture

- **Microservices Pattern**: Separated concerns into independent services
- **API Communication**: RESTful APIs with CORS support
- **File Storage**: Shared temporary storage with job-based organization
- **Progress Tracking**: Polling-based status updates (WebSocket support planned)

#### User Experience

- **Smart Downloads**: Single file downloads as CSV, multiple files as ZIP
- **Original Filenames**: Preserved in ZIP archives
- **Real-time Feedback**: Visual progress bars and status indicators
- **Error Handling**: Per-file error tracking and display
- **Theme Support**: Light, dark, and system theme options

#### Development

- **TypeScript**: Full type safety across frontend
- **Modern React**: Hooks, async operations, and optimistic updates
- **API Client**: Centralized API communication layer
- **Custom Hooks**: Reusable logic for upload, conversion, and download

### Fixed

- File status updates now properly track from upload through conversion
- Download functionality correctly routes to Download Service (was trying port 5000)
- Individual file downloads now work alongside batch downloads
- ZIP archives preserve original filenames (was using file IDs)
- Theme toggle icon properly changes color on hover

### Technical Details

#### Frontend Stack

- Next.js 15.5.6 with App Router
- React 19 with TypeScript 5
- Tailwind CSS v4
- shadcn/ui + Radix UI
- Zustand + React Query
- Lucide React icons

#### Backend Stack

- Flask 3.0.0
- pdfplumber 0.11.8 for PDF parsing
- Python 3.11+
- In-memory job tracking
- Temporary file system storage

#### Deployment

- Frontend: Ready for Vercel deployment
- Services: Containerized with Docker
- Local development: npm run dev (starts all services)
- Production: docker-compose with environment-specific configs

### Migration Status

- ✅ **Phase 1**: Project restructuring and documentation
- ✅ **Phase 2**: Frontend development with Next.js 15 + dark mode
- ✅ **Phase 3**: Backend microservices (Upload, Conversion, Download)
- 📋 **Phase 4**: Storage & Infrastructure improvements (S3, Redis)
- 📋 **Phase 5**: Testing & Documentation
- 📋 **Phase 6**: Production deployment & monitoring

### Breaking Changes

- **API Endpoints**: New service-specific URLs (5001, 5002, 5003)
- **Environment Variables**: New `NEXT_PUBLIC_*_SERVICE_URL` variables required
- **File IDs**: Now use UUIDs instead of timestamp-based IDs
- **Response Format**: Updated JSON structure for consistency

### Deprecated

- ❌ Legacy monolithic Flask app (moved to `/legacy` folder)
- ❌ Old API at port 5000
- ❌ In-app UI from Flask templates (replaced with Next.js)

---

## [0.0.1] - 2025-11-12

### Added

- Initial prototype of PDF to CSV converter (monolithic Flask application)
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

---

[0.1.0]: https://github.com/amin-bake/pdf-to-csv/releases/tag/v0.1.0
[0.0.1]: https://github.com/amin-bake/pdf-to-csv/releases/tag/v0.0.1
