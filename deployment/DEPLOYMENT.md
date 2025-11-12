# Production Deployment Guide

This guide provides recommendations for deploying the PDF to CSV converter in a production environment.

## ⚠️ Important Security Considerations

**This application is designed for development and demonstration purposes.** Before deploying to production, please implement the following security measures:

### 1. Authentication & Authorization

The current implementation has **no authentication**. For production:

```python
# Example: Add Flask-Login or Flask-HTTPAuth
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Implement your authentication logic
    pass

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload():
    # Your upload logic
    pass
```

### 2. File Upload Security

**Current limitations:**
- No file size limits
- No file type validation beyond accept attribute
- No virus scanning

**Recommendations:**

```python
# Add file size limit
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Validate file type
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# In upload route
if not allowed_file(file.filename):
    return jsonify({'error': 'Only PDF files allowed'}), 400
```

### 3. Rate Limiting

Implement rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
def upload():
    # Your logic
    pass
```

### 4. CORS Configuration

For API access from different domains:

```python
from flask_cors import CORS

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### 5. HTTPS/SSL

**Always use HTTPS in production.** Never run Flask's development server in production.

## 🚀 Production Server Setup

### Option 1: Gunicorn (Linux/Mac)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Create `wsgi.py`:
```python
from app import app

if __name__ == "__main__":
    app.run()
```

3. Run with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 wsgi:app
```

### Option 2: Waitress (Windows)

1. Install Waitress:
```powershell
pip install waitress
```

2. Create `wsgi.py`:
```python
from waitress import serve
from app import app

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000, threads=4)
```

3. Run:
```powershell
python wsgi.py
```

### Option 3: Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "wsgi:app"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./temp:/app/temp
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## 🗄️ File Storage & Cleanup

### Current Implementation
- Uses temporary files that persist until system cleanup
- In-memory dictionary for file metadata

### Production Recommendations

1. **Implement automatic cleanup**:

```python
import schedule
import time
from datetime import datetime, timedelta

def cleanup_old_files():
    """Remove files older than 1 hour"""
    cutoff = datetime.now() - timedelta(hours=1)
    for file_id, info in list(uploaded_files.items()):
        # Check file age and remove if old
        pass

schedule.every(30).minutes.do(cleanup_old_files)

# Run scheduler in background thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_scheduler, daemon=True).start()
```

2. **Use cloud storage** (S3, Azure Blob, Google Cloud Storage)
3. **Implement database** for file metadata (PostgreSQL, MongoDB)

## 📊 Monitoring & Logging

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('PDF to CSV startup')
```

### Error Tracking

Consider integrating:
- **Sentry** for error tracking
- **New Relic** or **DataDog** for APM
- **Prometheus** for metrics

## 🔒 Environment Variables

Never hardcode secrets. Use environment variables:

```python
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_FILE_SIZE', 16777216))
```

Create `.env` file (add to .gitignore):
```
SECRET_KEY=your-secret-key-here
MAX_FILE_SIZE=16777216
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

Load with python-dotenv:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🌐 Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
    }
}
```

## 📋 Production Checklist

- [ ] Replace Flask development server with production WSGI server
- [ ] Enable HTTPS/SSL
- [ ] Implement authentication and authorization
- [ ] Add file upload validation and limits
- [ ] Set up rate limiting
- [ ] Configure proper CORS policies
- [ ] Implement file cleanup mechanisms
- [ ] Set up logging and monitoring
- [ ] Use environment variables for configuration
- [ ] Set up automated backups (if using database)
- [ ] Configure reverse proxy (Nginx/Apache)
- [ ] Set up firewall rules
- [ ] Implement error tracking
- [ ] Add health check endpoint
- [ ] Write comprehensive tests
- [ ] Document API endpoints
- [ ] Create deployment scripts
- [ ] Set up CI/CD pipeline

## 🆘 Support

For production deployment assistance, please open an issue with the "deployment" label.
