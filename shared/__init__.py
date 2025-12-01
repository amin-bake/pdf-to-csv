"""Shared library package."""

__version__ = "1.0.0"

from .storage import StorageBackend, LocalStorageBackend, S3StorageBackend, get_storage_backend
from .utils import (
    generate_file_id,
    generate_hash,
    get_timestamp,
    format_file_size,
    create_api_response
)

__all__ = [
    'StorageBackend',
    'LocalStorageBackend',
    'S3StorageBackend',
    'get_storage_backend',
    'generate_file_id',
    'generate_hash',
    'get_timestamp',
    'format_file_size',
    'create_api_response',
]
