FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for pdfplumber
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Create directories
RUN mkdir -p /tmp/pdf-to-csv-uploads /tmp/pdf-to-csv-converted

# Expose port
EXPOSE 5002

# Run application
CMD ["python", "app.py"]
