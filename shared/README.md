# Shared Libraries

Common utilities and types shared across services.

## Structure

- `storage.py` - Storage backend abstraction (Local & S3)
- `types.py` - Common type definitions
- `utils.py` - Utility functions
- `constants.py` - Shared constants

## Usage

```python
from shared.storage import get_storage_backend
from shared.types import UploadedFile, ConversionStatus

storage = get_storage_backend()
```
