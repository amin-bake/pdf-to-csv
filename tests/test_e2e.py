"""
End-to-end test: upload a dummy PDF, convert it, poll status, and verify download.
Requires the Flask server to be running on http://127.0.0.1:5000
"""
import requests
import time
import io
import zipfile

BASE = 'http://127.0.0.1:5000'

def test_upload_convert_download():
    # 1. Create a minimal valid PDF with some text (pdfplumber can extract)
    # This is a very basic PDF structure with a single page containing text
    dummy_pdf = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources 4 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >>
endobj
5 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
50 700 Td
(Hello World) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000229 00000 n 
0000000327 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
420
%%EOF
"""
    
    # 2. Upload the file
    print("Uploading dummy PDF...")
    files = {'file': ('test.pdf', io.BytesIO(dummy_pdf), 'application/pdf')}
    r = requests.post(f'{BASE}/upload', files=files)
    assert r.status_code == 200, f"Upload failed: {r.status_code} {r.text}"
    upload_resp = r.json()
    file_id = upload_resp['id']
    print(f"  ✓ Uploaded successfully. File ID: {file_id}")
    
    # 3. Trigger conversion
    print("Triggering conversion...")
    r = requests.post(f'{BASE}/convert', json={
        'file_ids': [file_id],
        'parser': 'pdfplumber',
        'merge': False
    })
    assert r.status_code == 200, f"Convert failed: {r.status_code} {r.text}"
    convert_resp = r.json()
    assert convert_resp.get('started'), "Conversion did not start"
    print(f"  ✓ Conversion started for {len(convert_resp['file_ids'])} file(s)")
    
    # 4. Poll status until done or error
    print("Polling status...")
    max_wait = 30  # seconds
    start = time.time()
    final_status = None
    while time.time() - start < max_wait:
        r = requests.get(f'{BASE}/status/{file_id}')
        assert r.status_code == 200, f"Status check failed: {r.status_code}"
        status_data = r.json()
        print(f"  Status: {status_data['status']}, Progress: {status_data['progress']}%")
        if status_data['status'] in ('done', 'error'):
            final_status = status_data
            break
        time.sleep(0.5)
    
    assert final_status, "Conversion did not complete within timeout"
    print(f"  ✓ Conversion completed with status: {final_status['status']}")
    if final_status.get('error'):
        print(f"    Error: {final_status['error']}")
    print(f"    Converted files: {final_status.get('converted_files', [])}")
    
    # 5. Download the result
    if final_status['status'] == 'done':
        print("Downloading result...")
        r = requests.get(f'{BASE}/download/{file_id}')
        assert r.status_code == 200, f"Download failed: {r.status_code}"
        
        content_type = r.headers.get('Content-Type')
        num_files = len(final_status.get('converted_files', []))
        
        # Single file should return CSV, multiple files should return ZIP
        if num_files == 1:
            assert 'text/csv' in content_type, f"Expected CSV for single file, got {content_type}"
            print(f"  ✓ Single file returned as CSV ({len(r.content)} bytes)")
            print(f"    Content preview: {r.content.decode('utf-8')[:100]}")
        else:
            assert 'application/zip' in content_type, f"Expected ZIP for multiple files, got {content_type}"
            # Verify ZIP contents
            zip_data = io.BytesIO(r.content)
            with zipfile.ZipFile(zip_data, 'r') as zf:
                names = zf.namelist()
                print(f"  ✓ ZIP contains {len(names)} file(s): {names}")
                # Read first CSV
                if names:
                    csv_content = zf.read(names[0]).decode('utf-8')
                    print(f"    Preview of {names[0]}:")
                    print(f"      {csv_content[:200]}")
    
    print("\n✅ End-to-end test passed!")

if __name__ == '__main__':
    try:
        test_upload_convert_download()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Make sure Flask app is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
