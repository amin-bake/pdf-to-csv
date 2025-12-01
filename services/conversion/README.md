# Conversion Service

Flask microservice for PDF to CSV conversion.

## Endpoints

- `POST /api/v1/convert` - Start conversion
- `GET /api/v1/status/:id` - Check conversion status
- `DELETE /api/v1/convert/:id` - Cancel conversion
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
PORT=5002
STORAGE_BACKEND=local
UPLOAD_SERVICE_URL=http://localhost:5001
DOWNLOAD_SERVICE_URL=http://localhost:5003
```
