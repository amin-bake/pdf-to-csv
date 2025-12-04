"""
Download Service
Handles file downloads and ZIP creation for batch downloads.
Port: 5003
"""
import os
import zipfile
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
CONVERTED_FOLDER = os.path.join(tempfile.gettempdir(), 'pdf-to-csv-converted')

# Ensure directory exists
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


def find_file(file_id):
    """
    Find a file by searching through the converted folder structure.
    Returns the full path if found, None otherwise.
    """
    for root, dirs, files in os.walk(CONVERTED_FOLDER):
        for filename in files:
            if file_id in filename or filename.startswith(file_id):
                return os.path.join(root, filename)
    return None


def create_zip_archive(file_paths, zip_filename, file_names=None):
    """
    Create a ZIP archive from a list of file paths.
    
    Args:
        file_paths: List of file paths to include in the ZIP
        zip_filename: Name of the ZIP file to create
        file_names: Optional dict mapping file paths to desired names in ZIP
    
    Returns the path to the created ZIP file.
    """
    zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            if os.path.exists(file_path):
                # Use custom name if provided, otherwise use basename
                archive_name = file_names.get(file_path) if file_names else os.path.basename(file_path)
                zipf.write(file_path, archive_name)
    
    return zip_path


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'download',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """
    Download a single converted file.
    
    URL Parameters:
    - file_id: The unique identifier for the converted file
    """
    # Find the file
    file_path = find_file(file_id)
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({
            'success': False,
            'error': {
                'code': 'FILE_NOT_FOUND',
                'message': f'File {file_id} not found'
            }
        }), 404
    
    try:
        # Determine the correct MIME type based on file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext == '.xlsx':
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif file_ext == '.csv':
            mimetype = 'text/csv'
        elif file_ext == '.json':
            mimetype = 'application/json'
        elif file_ext == '.txt':
            mimetype = 'text/plain'
        else:
            mimetype = 'application/octet-stream'
        
        # Send file as attachment
        return send_file(
            file_path,
            as_attachment=True,
            download_name=os.path.basename(file_path),
            mimetype=mimetype
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'DOWNLOAD_FAILED',
                'message': str(e)
            }
        }), 500


@app.route('/api/download/batch', methods=['POST'])
def download_batch():
    """
    Download multiple files as a ZIP archive.
    
    Request body:
    {
        "fileIds": ["file1_id", "file2_id", ...],
        "fileNames": {"file1_id": "original_name.csv", ...},  // optional
        "zipName": "converted_files.zip"  // optional
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
    file_names_map = data.get('fileNames', {})
    zip_name = data.get('zipName', f'converted_files_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip')
    
    if not file_ids:
        return jsonify({
            'success': False,
            'error': {
                'code': 'NO_FILES',
                'message': 'No file IDs provided'
            }
        }), 400
    
    # Find all requested files
    file_paths = []
    file_path_to_name = {}
    missing_files = []
    
    for file_id in file_ids:
        file_path = find_file(file_id)
        if file_path and os.path.exists(file_path):
            file_paths.append(file_path)
            # Map file path to original name if provided
            if file_id in file_names_map:
                file_path_to_name[file_path] = file_names_map[file_id]
        else:
            missing_files.append(file_id)
    
    if not file_paths:
        return jsonify({
            'success': False,
            'error': {
                'code': 'NO_FILES_FOUND',
                'message': 'None of the requested files were found',
                'details': {'missingFiles': missing_files}
            }
        }), 404
    
    try:
        # Create ZIP archive with custom names
        zip_path = create_zip_archive(file_paths, zip_name, file_path_to_name if file_path_to_name else None)
        
        # Send ZIP file
        response = send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_name,
            mimetype='application/zip'
        )
        
        # Clean up ZIP file after sending (in production, use a cleanup job)
        # Note: The file will be deleted after the response is sent
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(zip_path):
                    os.remove(zip_path)
            except Exception:
                pass
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'ZIP_CREATION_FAILED',
                'message': str(e)
            }
        }), 500


@app.route('/api/files/<file_id>/info', methods=['GET'])
def get_file_info(file_id):
    """Get information about a converted file."""
    file_path = find_file(file_id)
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({
            'success': False,
            'error': {
                'code': 'FILE_NOT_FOUND',
                'message': f'File {file_id} not found'
            }
        }), 404
    
    try:
        stat = os.stat(file_path)
        
        return jsonify({
            'success': True,
            'data': {
                'fileId': file_id,
                'filename': os.path.basename(file_path),
                'size': stat.st_size,
                'createdAt': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modifiedAt': datetime.fromtimestamp(stat.st_mtime).isoformat()
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INFO_FAILED',
                'message': str(e)
            }
        }), 500


@app.route('/api/cleanup/<job_id>', methods=['DELETE'])
def cleanup_job(job_id):
    """Clean up all files associated with a conversion job."""
    job_folder = os.path.join(CONVERTED_FOLDER, job_id)
    
    if not os.path.exists(job_folder):
        return jsonify({
            'success': False,
            'error': {
                'code': 'JOB_NOT_FOUND',
                'message': f'Job {job_id} not found'
            }
        }), 404
    
    try:
        # Remove entire job folder
        import shutil
        shutil.rmtree(job_folder)
        
        return jsonify({
            'success': True,
            'data': {
                'message': f'Job {job_id} cleaned up successfully'
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'CLEANUP_FAILED',
                'message': str(e)
            }
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
