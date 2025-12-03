"""
Conversion Service
Handles PDF to CSV, Excel, and JSON conversion using pdfplumber and tabula.
Port: 5002
"""
import os
import tempfile
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS

from worker import ConversionWorker

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

# Initialize conversion worker
worker = ConversionWorker(UPLOAD_FOLDER, CONVERTED_FOLDER, conversion_jobs)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'conversion',
        'timestamp': datetime.now(timezone.utc).isoformat()
    })


@app.route('/api/convert', methods=['POST'])
def convert():
    """
    Start PDF to CSV/Excel/JSON conversion job.
    
    Request body:
    {
        "fileIds": ["abc123", "def456"],
        "parser": "pdfplumber",  // or "tabula"
        "merge": false,
        "outputFormat": "csv"  // or "excel" or "json"
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
    output_format = data.get('outputFormat', 'csv')
    
    if not file_ids:
        return jsonify({
            'success': False,
            'error': {
                'code': 'NO_FILES',
                'message': 'No files provided for conversion'
            }
        }), 400
    
    # Create conversion job using worker
    job_id = worker.start_conversion(file_ids, parser, merge, output_format)
    
    return jsonify({
        'success': True,
        'data': {
            'jobId': job_id,
            'status': 'pending',
            'message': 'Conversion started'
        },
        'timestamp': datetime.now(timezone.utc).isoformat()
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
        'timestamp': datetime.now(timezone.utc).isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
