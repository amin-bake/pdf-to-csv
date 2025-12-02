"""Common utility functions."""
import uuid
import hashlib
from datetime import datetime
from typing import Dict, Any


def generate_file_id() -> str:
    """Generate unique file ID."""
    return str(uuid.uuid4())


def generate_hash(data: bytes) -> str:
    """Generate SHA256 hash of data."""
    return hashlib.sha256(data).hexdigest()


def get_timestamp() -> str:
    """Get current ISO timestamp."""
    return datetime.utcnow().isoformat() + 'Z'


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def create_api_response(
    success: bool,
    data: Any = None,
    error: Dict[str, Any] = None,
    request_id: str = None
) -> Dict[str, Any]:
    """
    Create standardized API response.
    
    Args:
        success: Whether the request was successful
        data: Response data
        error: Error information
        request_id: Request identifier
    
    Returns:
        Formatted API response dictionary
    """
    response = {
        'success': success,
        'meta': {
            'timestamp': get_timestamp(),
            'requestId': request_id or generate_file_id(),
            'version': 'v1'
        }
    }
    
    if data is not None:
        response['data'] = data
    
    if error is not None:
        response['error'] = error
    
    return response
