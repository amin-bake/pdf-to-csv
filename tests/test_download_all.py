"""
Test for Download All endpoint - verifies that multiple files can be downloaded as a single ZIP.
"""
import requests
import io
import zipfile

BASE_URL = "http://localhost:5000"

def create_test_pdf(text_content):
    """Create a minimal PDF with text content."""
    # Minimal PDF structure
    pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
({text_content}) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000262 00000 n 
0000000356 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
444
%%EOF
"""
    return io.BytesIO(pdf_content.encode('latin-1'))

def upload_and_convert(filename, content):
    """Upload a PDF and convert it, return the file ID."""
    pdf_data = create_test_pdf(content)
    
    # Upload
    print(f"Uploading {filename}...")
    upload_response = requests.post(
        f"{BASE_URL}/upload",
        files={'file': (filename, pdf_data, 'application/pdf')}
    )
    upload_response.raise_for_status()
    file_id = upload_response.json()['id']
    print(f"✓ Uploaded {filename}: {file_id}")
    
    # Convert
    convert_response = requests.post(
        f"{BASE_URL}/convert",
        json={'file_ids': [file_id], 'parser': 'pdfplumber', 'merge': True}
    )
    convert_response.raise_for_status()
    
    # Wait for conversion
    import time
    for _ in range(20):
        status_response = requests.get(f"{BASE_URL}/status/{file_id}")
        status_data = status_response.json()
        if status_data['status'] == 'done':
            break
        time.sleep(0.5)
    
    return file_id

def main():
    print("Testing Download All endpoint...\n")
    
    # Upload and convert multiple files
    print("1. Uploading and converting multiple files...")
    file_id_1 = upload_and_convert("test1.pdf", "Content from file 1")
    file_id_2 = upload_and_convert("test2.pdf", "Content from file 2")
    file_id_3 = upload_and_convert("test3.pdf", "Content from file 3")
    
    file_ids = [file_id_1, file_id_2, file_id_3]
    print(f"✓ All files converted. IDs: {file_ids}\n")
    
    # Download all as ZIP
    print("2. Downloading all files as ZIP...")
    download_response = requests.post(
        f"{BASE_URL}/download_all",
        json={'file_ids': file_ids}
    )
    download_response.raise_for_status()
    
    # Verify it's a ZIP
    content_type = download_response.headers.get('Content-Type')
    print(f"Content-Type: {content_type}")
    
    if 'application/zip' not in content_type:
        print(f"❌ Expected ZIP file, got {content_type}")
        return False
    
    # Extract and verify ZIP contents
    zip_buffer = io.BytesIO(download_response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zf:
        file_list = zf.namelist()
        print(f"✓ ZIP contains {len(file_list)} file(s):")
        for fname in file_list:
            print(f"  - {fname}")
            # Read content
            content = zf.read(fname).decode('utf-8', errors='ignore')
            print(f"    Content preview: {content[:50]}...")
    
    if len(file_list) != 3:
        print(f"❌ Expected 3 files in ZIP, got {len(file_list)}")
        return False
    
    print("\n✅ Download All test passed!")
    print("   - Multiple files uploaded and converted successfully")
    print("   - Download All returned a single ZIP file")
    print("   - ZIP contains all converted CSV files")
    return True

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
