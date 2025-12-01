# Upload Service

Flask microservice for handling file uploads.

## Endpoints

- `POST /api/v1/upload` - Upload PDF file
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
PORT=5001
STORAGE_BACKEND=local
S3_BUCKET=your-bucket-name
CORS_ORIGINS=http://localhost:3000
```
