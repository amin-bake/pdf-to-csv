# Download Service

Flask microservice for handling file downloads.

## Endpoints

- `GET /api/v1/download/:id` - Download single file
- `POST /api/v1/download/batch` - Download multiple files as ZIP
- `GET /api/v1/download/:id/info` - Get file information
- `GET /health` - Health check

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Environment Variables

```
FLASK_ENV=development
PORT=5003
STORAGE_BACKEND=local
CONVERSION_SERVICE_URL=http://localhost:5002
```
