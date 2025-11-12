# Quick Reference Guide

Quick command reference for common tasks with the PDF to CSV converter.

## Development

### Setup

```powershell
# Clone repository
git clone https://github.com/YOUR_USERNAME/pdf-to-csv.git
cd pdf-to-csv

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Running

```powershell
# Development server
python app.py
# Access at http://localhost:5000

# Production server (Windows)
pip install waitress
python wsgi.py

# Production server (Linux/Mac)
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app
```

### Testing

```powershell
# Run all tests (ensure server is running first)
python test_e2e.py
python test_upload.py
python test_download_types.py
python test_download_all.py

# Or run in sequence
python test_e2e.py; python test_upload.py; python test_download_types.py; python test_download_all.py
```

## Git Workflow

### Initial Setup

```powershell
# Initialize repository
git init
git add .
git commit -m "Initial commit"
git branch -M main

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/pdf-to-csv.git
git push -u origin main
```

### Feature Development

```powershell
# Create feature branch
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "Add feature description"

# Push to GitHub
git push origin feature/feature-name

# Create Pull Request on GitHub
```

### Release Process

```powershell
# Update CHANGELOG.md with version and date
# Commit changes
git add CHANGELOG.md
git commit -m "Prepare v1.0.0 release"

# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0

# Create release on GitHub from tag
```

## Maintenance

### Update Dependencies

```powershell
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Security Audit

```powershell
# Install audit tools
pip install pip-audit safety

# Run security check
pip-audit
safety check -r requirements.txt
```

### Clean Environment

```powershell
# Remove virtual environment
deactivate
Remove-Item -Recurse -Force .venv

# Recreate and reinstall
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Docker

### Build and Run

```powershell
# Build image
docker build -t pdf-to-csv .

# Run container
docker run -p 8000:8000 pdf-to-csv

# Using docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## API Usage

### Upload File

```python
import requests

url = "http://localhost:5000/upload"
files = {'file': open('document.pdf', 'rb')}
response = requests.post(url, files=files)
file_id = response.json()['id']
```

### Convert File

```python
url = "http://localhost:5000/convert"
data = {
    'file_ids': [file_id],
    'parser': 'pdfplumber',
    'merge': True
}
response = requests.post(url, json=data)
```

### Check Status

```python
url = f"http://localhost:5000/status/{file_id}"
response = requests.get(url)
status = response.json()
```

### Download File

```python
url = f"http://localhost:5000/download/{file_id}"
response = requests.get(url)
with open('output.csv', 'wb') as f:
    f.write(response.content)
```

### Download All

```python
url = "http://localhost:5000/download_all"
data = {'file_ids': [file_id1, file_id2]}
response = requests.post(url, json=data)
with open('all_files.zip', 'wb') as f:
    f.write(response.content)
```

## Common Issues

### Port Already in Use

```powershell
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py
app.run(port=5001)
```

### Module Not Found

```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests Fail - Server Not Running

```powershell
# Start server in background
Start-Process python -ArgumentList "app.py" -NoNewWindow

# Wait a few seconds, then run tests
Start-Sleep -Seconds 5
python test_e2e.py
```

### Java Not Found (Tabula)

```powershell
# Install Java JRE/JDK
# Download from https://adoptium.net/

# Verify installation
java -version

# Restart application
```

## File Locations

### Uploaded Files

- Windows: `C:\Users\USERNAME\AppData\Local\Temp\`
- Linux/Mac: `/tmp/`

### Converted Files

- Same as uploaded files, in subdirectories

### Application Logs

- Console output (development mode)
- Configure file logging in production (see DEPLOYMENT.md)

## Environment Variables

### Setting Variables (PowerShell)

```powershell
$env:FLASK_ENV = "production"
$env:SECRET_KEY = "your-secret-key"
$env:MAX_FILE_SIZE = "16777216"
```

### Using .env File

```powershell
# Install python-dotenv
pip install python-dotenv

# Create .env file
SECRET_KEY=your-secret-key
MAX_FILE_SIZE=16777216

# Load in app.py
from dotenv import load_dotenv
load_dotenv()
```

## Performance Tuning

### Increase Workers

```powershell
# Gunicorn
gunicorn --workers 8 --threads 2 wsgi:app

# Waitress
waitress-serve --threads=8 wsgi:app
```

### Timeout Settings

```powershell
# Gunicorn (for large files)
gunicorn --timeout 300 wsgi:app
```

### Memory Limits

```powershell
# Docker
docker run -m 2g pdf-to-csv
```

## Useful Links

- **Documentation**: See README.md, DEPLOYMENT.md
- **Contributing**: See CONTRIBUTING.md
- **Issues**: GitHub Issues tab
- **Releases**: GitHub Releases tab
- **Security**: See SECURITY.md

---

For detailed information, consult the full documentation files in the repository.
