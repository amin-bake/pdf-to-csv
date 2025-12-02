"""
Conversion Service
Handles PDF to CSV conversion using pdfplumber and tabula.
Port: 5002
"""
import os
import uuid
import csv
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import tempfile

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'pdf-to-csv-uploads')
CONVERTED_FOLDER = os.path.join(tempfile.gettempdir(), 'pdf-to-csv-converted')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# In-memory storage for conversion jobs
conversion_jobs = {}


def extract_tables_pdfplumber(pdf_path):
    """
    Extract tables from PDF using pdfplumber.
    Returns list of tables (each table is a list of rows).
    """
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                for table in page_tables:
                    # Clean table: replace None with empty string
                    clean_table = [
                        [cell if cell is not None else "" for cell in row]
                        for row in table
                    ]
                    tables.append(clean_table)
    return tables


def extract_text_lines(pdf_path):
    """
    Fallback: Extract text lines when no tables found.
    Returns list of single-column rows.
    """
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ''
            for line in text.splitlines():
                if line.strip():
                    lines.append([line])
    return [lines] if lines else []


def save_tables_to_csv(tables, output_dir, base_filename, merge=False):
    """
    Save extracted tables to CSV files.
    Returns list of created file paths.
    """
    converted_files = []
    
    if merge:
        # Merge all tables into a single CSV
        output_path = os.path.join(output_dir, f"{base_filename}.csv")
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for table in tables:
                for row in table:
                    writer.writerow(row)
        converted_files.append(output_path)
    else:
        # Save each table as a separate CSV
        for idx, table in enumerate(tables, start=1):
            output_path = os.path.join(output_dir, f"{base_filename}_table{idx}.csv")
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in table:
                    writer.writerow(row)
            converted_files.append(output_path)
    
    return converted_files


def process_conversion(job_id, file_infos, parser, merge):
    """
    Background worker to process PDF conversion.
    Updates job status as it progresses.
    """
    job = conversion_jobs[job_id]
    job['status'] = 'processing'
    job['progress'] = 0
    
    try:
        total_files = len(file_infos)
        all_converted = []
        
        for idx, file_info in enumerate(file_infos):
            file_id = file_info['fileId']
            filename = file_info['filename']
            
            # Find the PDF file
            pdf_path = None
            for f in os.listdir(UPLOAD_FOLDER):
                if f.startswith(file_id):
                    pdf_path = os.path.join(UPLOAD_FOLDER, f)
                    break
            
            if not pdf_path or not os.path.exists(pdf_path):
                job['errors'].append(f"File not found: {filename}")
                continue
            
            # Update status
            job['status'] = 'converting'
            job['currentFile'] = filename
            
            # Extract tables
            if parser == 'pdfplumber':
                tables = extract_tables_pdfplumber(pdf_path)
                
                # Fallback to text if no tables found
                if not tables:
                    tables = extract_text_lines(pdf_path)
            else:
                # Future: Add tabula support
                tables = extract_tables_pdfplumber(pdf_path)
            
            # Create output directory for this file
            base_filename = os.path.splitext(filename)[0]
            file_output_dir = os.path.join(CONVERTED_FOLDER, job_id, file_id)
            os.makedirs(file_output_dir, exist_ok=True)
            
            # Save to CSV
            if tables:
                converted_files = save_tables_to_csv(
                    tables, 
                    file_output_dir, 
                    base_filename, 
                    merge
                )
                
                for csv_path in converted_files:
                    all_converted.append({
                        'fileId': f"{file_id}_{os.path.basename(csv_path)}",
                        'originalFileId': file_id,
                        'filename': os.path.basename(csv_path),
                        'filepath': csv_path,
                        'size': os.path.getsize(csv_path)
                    })
            else:
                job['errors'].append(f"No tables extracted from: {filename}")
            
            # Update progress
            job['progress'] = int(((idx + 1) / total_files) * 100)
        
        # Mark as completed
        job['status'] = 'completed'
        job['progress'] = 100
        job['convertedFiles'] = all_converted
        job['completedAt'] = datetime.utcnow().isoformat()
        job['message'] = f"Successfully converted {len(all_converted)} file(s)"
        
    except Exception as e:
        job['status'] = 'error'
        job['progress'] = 100
        job['error'] = str(e)
        job['message'] = f"Conversion failed: {str(e)}"


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'conversion',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/convert', methods=['POST'])
def convert():
    """
    Start PDF to CSV conversion job.
    
    Request body:
    {
        "fileIds": ["abc123", "def456"],
        "parser": "pdfplumber",  // or "tabula"
        "merge": false
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INVALID_REQUEST',
                'message': 'Request body is required'
            }
        }), 400
    
    file_ids = data.get('fileIds', [])
    parser = data.get('parser', 'pdfplumber')
    merge = data.get('merge', False)
    
    if not file_ids:
        return jsonify({
            'success': False,
            'error': {
                'code': 'NO_FILES',
                'message': 'No files provided for conversion'
            }
        }), 400
    
    # Create conversion job
    job_id = uuid.uuid4().hex
    
    # Build file info list (assuming we get fileIds from upload service)
    file_infos = []
    for file_id in file_ids:
        # In production, we would fetch metadata from upload service
        # For now, we'll construct minimal info
        file_infos.append({
            'fileId': file_id,
            'filename': f"{file_id}.pdf"  # Will be updated when we find the actual file
        })
    
    conversion_jobs[job_id] = {
        'jobId': job_id,
        'status': 'pending',
        'progress': 0,
        'fileIds': file_ids,
        'parser': parser,
        'merge': merge,
        'createdAt': datetime.utcnow().isoformat(),
        'currentFile': None,
        'convertedFiles': [],
        'errors': [],
        'error': None,
        'message': 'Conversion queued'
    }
    
    # Start background conversion
    thread = threading.Thread(
        target=process_conversion,
        args=(job_id, file_infos, parser, merge),
        daemon=True
    )
    thread.start()
    
    return jsonify({
        'success': True,
        'data': {
            'jobId': job_id,
            'status': 'pending',
            'message': 'Conversion started'
        },
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get conversion job status."""
    if job_id not in conversion_jobs:
        return jsonify({
            'success': False,
            'error': {
                'code': 'JOB_NOT_FOUND',
                'message': 'Conversion job not found'
            }
        }), 404
    
    job = conversion_jobs[job_id]
    
    return jsonify({
        'success': True,
        'data': {
            'jobId': job['jobId'],
            'status': job['status'],
            'progress': job['progress'],
            'message': job.get('message', ''),
            'currentFile': job.get('currentFile'),
            'convertedFiles': job.get('convertedFiles', []),
            'errors': job.get('errors', []),
            'error': job.get('error'),
            'createdAt': job['createdAt'],
            'completedAt': job.get('completedAt')
        },
        'timestamp': datetime.utcnow().isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
