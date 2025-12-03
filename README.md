# PDF to CSV Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)

A modern, scalable web application that converts PDF files to CSV format using microservices architecture. Built with Next.js frontend and Flask microservices, featuring real-time progress tracking, drag-and-drop interface, and cloud-ready deployment.

<img width="1893" height="933" alt="image" src="https://github.com/user-attachments/assets/a582a824-81dd-4588-897c-4d4f4fd9be44" />

## 🏗️ Architecture

This project uses a **microservices architecture** with the following components:

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and shadcn/ui
- **Upload Service**: Handles file uploads and validation (Port 5001)
- **Conversion Service**: PDF to CSV conversion with pdfplumber/Tabula (Port 5002)
- **Download Service**: Manages file downloads and batch operations (Port 5003)
- **Shared Libraries**: Common utilities, storage abstraction, and type definitions

### Directory Structure

````
pdf-to-csv/
├── frontend/              # Next.js frontend application
│   ├── app/              # Next.js App Router
│   ├── components/       # React components
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utilities and API client
│   └── store/            # Zustand state management
├── services/
│   ├── upload/           # Upload microservice
│   ├── conversion/       # Conversion microservice
│   └── download/         # Download microservice
├── shared/               # Shared Python libraries
│   ├── storage.py        # Storage backend abstraction
│   ├── types.py          # Common type definitions
│   └── utils.py          # Utility functions
├── infrastructure/       # Docker & Kubernetes configs
├── docs/                 # Comprehensive documentation
│   ├── MIGRATION_PLAN.md
│   ├── ARCHITECTURE.md
│   ├── API_SPECIFICATION.md
│   ├── FRONTEND_COMPONENTS.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── DOCKER_KUBERNETES.md
├── legacy/              # Original Flask monolith (deprecated)
└── docker-compose.yml   # Development environment

## ✨ Features

- 🏗️ **Microservices Architecture**: Scalable, independently deployable services
- 📤 **Multiple File Upload**: Drag & drop or select multiple PDF files at once
- 📊 **Smart Table Extraction**: Automatically detects and extracts tables from PDFs
- 📑 **Multiple Output Formats**: Convert to CSV, Excel (.xlsx), or JSON formats
- 🔄 **Automatic Merging**: Combines all tables from each PDF into a single output file
- 📈 **Real-time Progress**: Visual progress bars with status polling
- ⬇️ **Flexible Downloads**: Download files individually or all at once as a ZIP
- 🎯 **Dual Parser Support**: Choose between pdfplumber (default) or Tabula
- 💻 **Modern UI**: Next.js with Tailwind CSS and shadcn/ui components
- 🎨 **Multiple Color Themes**: Switch between "Earthy Forest" (green), "Cherry Blossom Bloom" (red/pink), and "Pastel Rainbow Fantasy" (dreamy pastels)
- 🌓 **Dark Mode Support**: Full light/dark mode for all color themes
- ⚡ **Background Processing**: Async conversion with React Query
- 🐳 **Docker Ready**: Complete containerization with docker-compose
- ☁️ **Cloud Native**: Deploy frontend to Vercel, backend to any cloud provider
- 📦 **Storage Abstraction**: Local filesystem or S3-compatible storage

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **(Optional)** Docker & Docker Compose
- **(Optional)** Java Runtime for Tabula parser

### Option 1: Local Development (Recommended)

1. **Clone the repository**

   ```powershell
   git clone https://github.com/amin-bake/pdf-to-csv.git
   cd pdf-to-csv
````

2. **Install root dependencies**

   ```powershell
   npm install
   ```

3. **Set up Frontend**

   ```powershell
   cd frontend
   npm install
   cp .env.local.example .env.local
   cd ..
   ```

4. **Set up Backend Services**

   ```powershell
   # Upload Service
   cd services/upload
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   cd ../..

   # Repeat for conversion and download services
   ```

5. **Run All Services**

   ```powershell
   # From root directory
   npm run dev
   ```

   This starts:

   - Frontend: http://localhost:3000
   - Upload Service: http://localhost:5001
   - Conversion Service: http://localhost:5002
   - Download Service: http://localhost:5003

### Option 2: Docker Compose

```powershell
# Build and start all services
docker-compose up --build

# Frontend will be available at http://localhost:3000
```

### Running the Application (Legacy)

```powershell
python app.py
```

Then open your browser and navigate to **http://localhost:5000**

## 📖 Usage

1. **Choose Conversion Type**: Select PDF to CSV, PDF to Excel, or PDF to JSON from the homepage
2. **Upload Files**: Drag & drop PDF files or click to browse
3. **Select Parser**: Choose between pdfplumber (default) or Tabula
4. **Choose Output Options**:
   - Select output format (CSV, Excel, or JSON)
   - Optionally merge all tables into a single file
5. **Convert**: Click "Convert" to start processing
6. **Monitor Progress**: Watch real-time conversion status
7. **Download**: Download individual files or all files as ZIP

### Conversion Formats

- **PDF to CSV**: Extract tables to comma-separated values format
  - Great for data analysis and spreadsheet import
  - Lightweight and universally compatible
- **PDF to Excel**: Extract tables to Excel spreadsheets (.xlsx)

  - Multiple tables saved as separate sheets when merged
  - Auto-adjusted column widths for better readability
  - Native Excel format with formatting support

- **PDF to JSON**: Extract tables to structured JSON format
  - **Tabular data**: First row used as object keys (headers)
  - **Non-tabular documents**: Full text extraction for CVs, resumes, reports
  - Tables preserved with metadata (table number, row/column counts, headers)
  - Automatic header cleaning (removes newlines, ensures uniqueness)
  - Empty rows and columns filtered out
  - Intelligent structure detection distinguishes titles, headers, and data
  - Perfect for web APIs and data interchange
  - Human-readable with proper indentation
  - Native Excel format with formatting support

### Parser Options

- **pdfplumber** (default): Works well with most PDFs, no additional dependencies
- **Tabula**: Better for complex table layouts, requires Java runtime

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

Comprehensive documentation is available in the `/docs` directory:

- **[MIGRATION_PLAN.md](docs/MIGRATION_PLAN.md)**: 8-week migration strategy from monolith to microservices
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Detailed technical architecture and design decisions
- **[API_SPECIFICATION.md](docs/API_SPECIFICATION.md)**: Complete RESTful API documentation
- **[FRONTEND_COMPONENTS.md](docs/FRONTEND_COMPONENTS.md)**: React component specifications
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)**: Deployment instructions for all platforms
- **[DOCKER_KUBERNETES.md](docs/DOCKER_KUBERNETES.md)**: Container orchestration configurations

## 🔌 API Endpoints

### Upload Service (Port 5001)

- `POST /api/v1/upload` - Upload PDF file
- `GET /health` - Health check

### Conversion Service (Port 5002)

- `POST /api/v1/convert` - Start conversion job
- `GET /api/v1/status/:id` - Check conversion status
- `DELETE /api/v1/convert/:id` - Cancel conversion
- `GET /health` - Health check

### Download Service (Port 5003)

- `GET /api/v1/download/:id` - Download converted file
- `POST /api/v1/download/batch` - Download multiple files as ZIP
- `GET /api/v1/download/:id/info` - Get file metadata
- `GET /health` - Health check

See [API_SPECIFICATION.md](docs/API_SPECIFICATION.md) for complete API documentation.

## 🧪 Testing

```powershell
# Frontend tests
cd frontend
npm test

# Backend tests
pytest services/

# E2E tests
pytest tests/test_e2e.py
```

## 🐳 Docker Deployment

### Development

```powershell
docker-compose up
```

### Production

```powershell
docker-compose -f docker-compose.prod.yml up -d
```

## ☁️ Cloud Deployment

### Frontend (Vercel)

```powershell
cd frontend
vercel --prod
```

### Backend Services

- **AWS ECS/Fargate**: See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md#aws-ecs)
- **Google Cloud Run**: See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md#google-cloud-run)
- **Kubernetes**: See [DOCKER_KUBERNETES.md](docs/DOCKER_KUBERNETES.md#kubernetes-deployment)

- **AWS ECS/Fargate**: See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md#aws-ecs)
- **Google Cloud Run**: See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md#google-cloud-run)
- **Kubernetes**: See [DOCKER_KUBERNETES.md](docs/DOCKER_KUBERNETES.md#kubernetes-deployment)

## 🗺️ Project Status

### Current Version: 0.1.0

✅ **Microservices architecture implemented!**

The application has been successfully migrated from a monolithic Flask application to a modern microservices architecture with Next.js frontend.

### Completed Phases

- ✅ **Phase 1**: Project restructuring and documentation
- ✅ **Phase 2**: Frontend development (Next.js 15 + TypeScript + Tailwind v4 + Dark Mode)
- ✅ **Phase 3**: Backend microservices (Upload, Conversion, Download services)

### Next Steps

- 📋 **Phase 4**: Storage & Infrastructure improvements (S3, Redis, persistent storage)
- 📋 **Phase 5**: Testing & Documentation (E2E tests, API docs, monitoring)
- 📋 **Phase 6**: Production deployment (CI/CD, scaling, observability)

### Architecture Highlights

- **Frontend**: Next.js 15 with modern React patterns and full TypeScript
- **Backend**: Three independent Flask microservices with health checks
- **Communication**: RESTful APIs with CORS support
- **Storage**: Shared file system (ready for S3 migration)
- **Deployment**: Docker Compose for local dev, cloud-ready for production

See [docs/PHASE_3_COMPLETE.md](docs/PHASE_3_COMPLETE.md) for detailed implementation notes.

## 🛠️ Technology Stack

### Frontend

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS v4
- **Components**: shadcn/ui (Radix UI)
- **State**: Zustand + React Query
- **Icons**: Lucide React

### Backend

- **Framework**: Flask 3.0
- **Language**: Python 3.11
- **PDF Parsing**: pdfplumber, Tabula-py
- **Storage**: Local filesystem / S3
- **Server**: Gunicorn

### Infrastructure

- **Containerization**: Docker
- **Orchestration**: Docker Compose / Kubernetes
- **CI/CD**: GitHub Actions
- **Hosting**: Vercel (Frontend), Cloud providers (Backend)

## 📝 Environment Variables

### Frontend (.env.local)

```bash
NEXT_PUBLIC_UPLOAD_SERVICE_URL=http://localhost:5001
NEXT_PUBLIC_CONVERSION_SERVICE_URL=http://localhost:5002
NEXT_PUBLIC_DOWNLOAD_SERVICE_URL=http://localhost:5003
NEXT_PUBLIC_MAX_FILE_SIZE=52428800
```

### Backend Services

```bash
FLASK_ENV=development
STORAGE_BACKEND=local
S3_BUCKET=your-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
CORS_ORIGINS=http://localhost:3000
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- PDF parsing by [pdfplumber](https://github.com/jsvine/pdfplumber)
- Alternative parsing with [Tabula](https://github.com/tabulapdf/tabula-py)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons by [Lucide](https://lucide.dev/)

## 📞 Support

For questions, issues, or feature requests:

- 🐛 [Open an issue](https://github.com/amin-bake/pdf-to-csv/issues)
- 💬 [Start a discussion](https://github.com/amin-bake/pdf-to-csv/discussions)
- 📧 Contact: your-email@example.com

## 🗺️ Roadmap

### Completed ✅

- [x] Initial Flask prototype (v0.0.1)
- [x] Microservices architecture design
- [x] Complete documentation suite
- [x] Next.js 15 frontend with TypeScript
- [x] Dark mode with theme toggle
- [x] Upload microservice with validation
- [x] Conversion microservice with pdfplumber
- [x] Download microservice with ZIP support
- [x] Docker Compose development environment
- [x] Health checks for all services

### In Progress 🚧

- [ ] Storage abstraction (S3 support)
- [ ] Redis for job queue management
- [ ] Comprehensive test suite
- [ ] API documentation (OpenAPI/Swagger)

### Planned 📋

- [ ] Production deployment (Vercel + AWS/GCP)
- [ ] Real-time WebSocket updates
- [ ] User authentication & authorization
- [ ] File history and management dashboard
- [ ] OCR support for scanned PDFs
- [ ] API rate limiting
- [ ] Monitoring & observability (Datadog/New Relic)
- [ ] CI/CD pipeline automation
- [ ] Horizontal scaling configuration
- [ ] Additional output formats (Excel, JSON)
- [ ] Comprehensive monitoring

---

**Made with ❤️ for the open-source community**

# Download behavior test

python test_download_types.py

# Download all test

python test_download_all.py

```

## 🔧 Configuration

The application uses in-memory storage for uploaded files and temporary directories for converted files. For production use, consider:

- Using a production WSGI server (gunicorn, waitress)
- Implementing file cleanup mechanisms
- Adding authentication/authorization
- Setting up proper logging
- Configuring file size limits

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and test thoroughly
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to your branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF table extraction
- [Tabula](https://github.com/tabulapedia/tabula-py) - Alternative parser
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [pandas](https://pandas.pydata.org/) - Data manipulation

## 📧 Support

If you encounter any issues or have questions:

- Open an [issue](https://github.com/YOUR_USERNAME/pdf-to-csv/issues)
- Check existing issues for solutions
- Read the [Contributing Guidelines](CONTRIBUTING.md)

## 🗺️ Roadmap

Potential future enhancements:

- [ ] Support for more output formats (Excel, JSON)
- [ ] Advanced table detection options
- [ ] Batch processing queue for large files
- [ ] Cloud storage integration
- [ ] API authentication
- [ ] Docker containerization
- [ ] Persistent storage option

---

Made with ❤️ by Mohamed Ali
```
