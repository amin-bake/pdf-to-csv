"""Storage backend abstraction for local and S3 storage."""
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

try:
    import boto3
    from botocore.exceptions import ClientError
    S3_AVAILABLE = True
except ImportError:
    S3_AVAILABLE = False


class StorageBackend(ABC):
    """Abstract base class for storage backends."""
    
    @abstractmethod
    def save(self, key: str, data: bytes) -> str:
        """Save data to storage and return the storage path."""
        pass
    
    @abstractmethod
    def load(self, key: str) -> bytes:
        """Load data from storage."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete data from storage."""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in storage."""
        pass


class LocalStorageBackend(StorageBackend):
    """Local filesystem storage backend."""
    
    def __init__(self, base_path: str = "./data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, data: bytes) -> str:
        file_path = self.base_path / key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        return str(file_path)
    
    def load(self, key: str) -> bytes:
        file_path = self.base_path / key
        return file_path.read_bytes()
    
    def delete(self, key: str) -> None:
        file_path = self.base_path / key
        if file_path.exists():
            file_path.unlink()
    
    def exists(self, key: str) -> bool:
        return (self.base_path / key).exists()


class S3StorageBackend(StorageBackend):
    """Amazon S3 storage backend."""
    
    def __init__(self):
        if not S3_AVAILABLE:
            raise ImportError("boto3 is required for S3 storage")
        
        self.s3_client = boto3.client(
            's3',
            region_name=os.getenv('S3_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.bucket = os.getenv('S3_BUCKET')
        
        if not self.bucket:
            raise ValueError("S3_BUCKET environment variable is required")
    
    def save(self, key: str, data: bytes) -> str:
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data
        )
        return f"s3://{self.bucket}/{key}"
    
    def load(self, key: str) -> bytes:
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket,
                Key=key
            )
            return response['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise FileNotFoundError(f"Key not found: {key}")
            raise
    
    def delete(self, key: str) -> None:
        self.s3_client.delete_object(
            Bucket=self.bucket,
            Key=key
        )
    
    def exists(self, key: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False


def get_storage_backend(backend_type: Optional[str] = None) -> StorageBackend:
    """
    Get storage backend instance based on configuration.
    
    Args:
        backend_type: Override backend type ('local' or 's3')
    
    Returns:
        StorageBackend instance
    """
    backend = backend_type or os.getenv('STORAGE_BACKEND', 'local')
    
    if backend == 's3':
        return S3StorageBackend()
    elif backend == 'local':
        return LocalStorageBackend()
    else:
        raise ValueError(f"Unknown storage backend: {backend}")
