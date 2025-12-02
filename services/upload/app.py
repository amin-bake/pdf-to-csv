"""
Upload Service
Handles file uploads, validation, and temporary storage.
Port: 5001
"""
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'pdf-to-csv-uploads')
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for uploaded file metadata
uploaded_files = {}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size(file_storage):
    """Get file size from FileStorage object."""
    file_storage.seek(0, 2)  # Seek to end
    size = file_storage.tell()
    file_storage.seek(0)  # Reset to beginning
    return size


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'upload',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/upload', methods=['POST'])
def upload():
    """
    Upload a single PDF file.
    Returns file metadata including unique file ID.
    """
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': {
                'code': 'NO_FILE',
                'message': 'No file provided'
            }
        }), 400

    file = request.files['file']

    # Check if file has a name
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': {
                'code': 'EMPTY_FILENAME',
                'message': 'No file selected'
            }
        }), 400

    # Validate file extension
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': {
                'code': 'INVALID_FILE_TYPE',
                'message': 'Only PDF files are allowed'
            }
        }), 400

    # Check file size
    file_size = get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        return jsonify({
            'success': False,
            'error': {
                'code': 'FILE_TOO_LARGE',
                'message': f'File size exceeds {MAX_FILE_SIZE / (1024 * 1024)}MB limit'
            }
        }), 400

    try:
        # Generate unique file ID
        file_id = uuid.uuid4().hex

        # Secure the filename
        original_filename = secure_filename(file.filename)
        
        # Create unique filename with file_id prefix
        filename = f"{file_id}_{original_filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Save file
        file.save(filepath)

        # Store metadata
        uploaded_files[file_id] = {
            'fileId': file_id,
            'filename': original_filename,
            'filepath': filepath,
            'size': file_size,
            'uploadedAt': datetime.utcnow().isoformat(),
            'status': 'uploaded'
        }

        return jsonify({
            'success': True,
            'data': {
                'fileId': file_id,
                'filename': original_filename,
                'size': file_size,
                'uploadedAt': uploaded_files[file_id]['uploadedAt']
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'UPLOAD_FAILED',
                'message': str(e)
            }
        }), 500


@app.route('/api/files/<file_id>', methods=['GET'])
def get_file_info(file_id):
    """Get metadata for an uploaded file."""
    if file_id not in uploaded_files:
        return jsonify({
            'success': False,
            'error': {
                'code': 'FILE_NOT_FOUND',
                'message': 'File not found'
            }
        }), 404

    file_info = uploaded_files[file_id]
    return jsonify({
        'success': True,
        'data': {
            'fileId': file_info['fileId'],
            'filename': file_info['filename'],
            'size': file_info['size'],
            'uploadedAt': file_info['uploadedAt'],
            'status': file_info['status']
        },
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete an uploaded file."""
    if file_id not in uploaded_files:
        return jsonify({
            'success': False,
            'error': {
                'code': 'FILE_NOT_FOUND',
                'message': 'File not found'
            }
        }), 404

    try:
        file_info = uploaded_files[file_id]
        
        # Delete physical file
        if os.path.exists(file_info['filepath']):
            os.remove(file_info['filepath'])
        
        # Remove from metadata
        del uploaded_files[file_id]

        return jsonify({
            'success': True,
            'data': {
                'message': 'File deleted successfully'
            },
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'DELETE_FAILED',
                'message': str(e)
            }
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
