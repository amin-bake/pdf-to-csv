"""Common type definitions shared across services."""
from typing import TypedDict, Literal, Optional, List
from datetime import datetime


FileStatus = Literal['uploading', 'uploaded', 'converting', 'completed', 'error']
ParserType = Literal['pdfplumber', 'tabula']


class UploadedFile(TypedDict):
    """Uploaded file metadata."""
    fileId: str
    fileName: str
    fileSize: int
    uploadedAt: str
    storagePath: str


class ConversionJob(TypedDict):
    """Conversion job metadata."""
    jobId: str
    fileId: str
    parser: ParserType
    merge: bool
    status: FileStatus
    progress: int
    createdAt: str
    updatedAt: str
    currentStep: Optional[str]
    error: Optional[str]


class ConvertedFile(TypedDict):
    """Converted file metadata."""
    fileId: str
    fileName: str
    fileSize: int
    downloadUrl: str


class ConversionResult(TypedDict):
    """Result of conversion operation."""
    jobId: str
    status: FileStatus
    files: List[ConvertedFile]
    error: Optional[str]


class ApiResponse(TypedDict):
    """Standard API response format."""
    success: bool
    data: Optional[dict]
    error: Optional[dict]
    meta: dict
