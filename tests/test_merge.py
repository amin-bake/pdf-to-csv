"""
Test the merge option: upload a PDF, convert with merge=True and merge=False, compare results.
"""
import requests
import time
import io
import zipfile

BASE = 'http://127.0.0.1:5000'

# A minimal PDF with text that might be extracted as separate "tables" or text blocks
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
<< /Length 88 >>
stream
BT
/F1 12 Tf
50 700 Td
(Line 1) Tj
0 -20 Td
(Line 2) Tj
0 -20 Td
(Line 3) Tj
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
464
%%EOF
"""

def upload_file():
    files = {'file': ('test_merge.pdf', io.BytesIO(dummy_pdf), 'application/pdf')}
    r = requests.post(f'{BASE}/upload', files=files)
    assert r.status_code == 200
    return r.json()['id']

def convert_and_wait(file_id, merge):
    r = requests.post(f'{BASE}/convert', json={
        'file_ids': [file_id],
        'parser': 'pdfplumber',
        'merge': merge
    })
    assert r.status_code == 200
    
    # Poll until done
    for _ in range(60):
        r = requests.get(f'{BASE}/status/{file_id}')
        status_data = r.json()
        if status_data['status'] in ('done', 'error'):
            return status_data
        time.sleep(0.5)
    raise TimeoutError("Conversion timeout")

def download_zip(file_id):
    r = requests.get(f'{BASE}/download/{file_id}')
    assert r.status_code == 200
    zip_data = io.BytesIO(r.content)
    with zipfile.ZipFile(zip_data, 'r') as zf:
        return {name: zf.read(name).decode('utf-8') for name in zf.namelist()}

print("Test 1: Convert without merge")
fid1 = upload_file()
status1 = convert_and_wait(fid1, merge=False)
print(f"  Status: {status1['status']}, Files: {status1['converted_files']}")
if status1['status'] == 'done':
    files1 = download_zip(fid1)
    print(f"  Downloaded {len(files1)} file(s): {list(files1.keys())}")
    for name, content in files1.items():
        print(f"    {name}: {len(content)} bytes")

print("\nTest 2: Convert with merge=True")
fid2 = upload_file()
status2 = convert_and_wait(fid2, merge=True)
print(f"  Status: {status2['status']}, Files: {status2['converted_files']}")
if status2['status'] == 'done':
    files2 = download_zip(fid2)
    print(f"  Downloaded {len(files2)} file(s): {list(files2.keys())}")
    for name, content in files2.items():
        print(f"    {name}: {len(content)} bytes")
        print(f"    Content preview: {content[:100]}")

print("\n✅ Merge test completed!")
