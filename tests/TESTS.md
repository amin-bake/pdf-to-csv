# PDF to CSV Converter - Test Suite

This directory contains automated tests for the PDF to CSV converter application.

## Test Files

### test_e2e.py
End-to-end integration test that validates the complete workflow:
- Upload a PDF file
- Trigger conversion
- Poll status until completion
- Download the result
- Verify the content

**Run:** `python test_e2e.py`

### test_upload.py
Tests the file upload functionality:
- Single file upload
- Multiple file uploads
- File metadata handling
- Error cases

**Run:** `python test_upload.py`

### test_download_types.py
Tests the smart download behavior:
- Single file returns CSV directly
- Multiple files return ZIP
- Content-Type headers
- Filename handling

**Run:** `python test_download_types.py`

### test_download_all.py
Tests the "Download All" feature:
- Multiple file conversions
- Single ZIP archive creation
- ZIP content verification
- Error handling

**Run:** `python test_download_all.py`

## Running Tests

### Prerequisites

Ensure the Flask application is running:
```powershell
python app.py
```

### Run All Tests

```powershell
python test_e2e.py
python test_upload.py
python test_download_types.py
python test_download_all.py
```

### Expected Output

Each test should output progress messages and end with:
- `✅ Test passed!` - Test completed successfully
- `❌ Test failed` - Test encountered an error

## Adding New Tests

When adding new tests:

1. Create a new test file with descriptive name (e.g., `test_feature_name.py`)
2. Import required libraries (`requests`, `io`, etc.)
3. Set `BASE_URL = "http://localhost:5000"`
4. Write test functions with clear descriptions
5. Add proper error handling and assertions
6. Print progress messages for debugging
7. Return boolean success status
8. Update this README with test description

### Test Template

```python
"""
Test description here
"""
import requests

BASE_URL = "http://localhost:5000"

def test_feature():
    """Test a specific feature"""
    print("Testing feature...")
    
    # Your test logic here
    response = requests.get(f"{BASE_URL}/endpoint")
    assert response.status_code == 200
    
    print("✅ Test passed!")
    return True

if __name__ == '__main__':
    try:
        success = test_feature()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        exit(1)
```

## Test Coverage

Current test coverage:
- ✅ File upload (single and multiple)
- ✅ Conversion process
- ✅ Status polling
- ✅ Individual downloads
- ✅ Batch downloads (ZIP)
- ✅ Content verification
- ✅ Error handling

Areas for future testing:
- [ ] Parser selection (Tabula vs pdfplumber)
- [ ] Large file handling
- [ ] Concurrent uploads
- [ ] Error scenarios (invalid PDFs, missing files)
- [ ] Performance benchmarks
- [ ] Browser automation tests

## CI/CD Integration

To integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python app.py &
      - run: sleep 5
      - run: python test_e2e.py
      - run: python test_upload.py
      - run: python test_download_types.py
      - run: python test_download_all.py
```

## Troubleshooting

### Server Not Running
```
Error: Failed to connect to http://localhost:5000
Solution: Start the Flask app with `python app.py`
```

### Port Already in Use
```
Error: Address already in use
Solution: Kill the process using port 5000 or change the port
```

### Import Errors
```
Error: No module named 'requests'
Solution: Install dependencies with `pip install -r requirements.txt`
```

## Contributing

When contributing tests:
1. Ensure tests are independent and can run in any order
2. Clean up any resources (files, connections) after tests
3. Use descriptive test names and comments
4. Follow the existing test structure
5. Update this README with your changes
