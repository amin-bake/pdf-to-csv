"""
PDF Extraction Module
Handles raw data extraction from PDF files using different parsers.
"""
import pdfplumber


def extract_tables_pdfplumber(pdf_path):
    """
    Extract tables from PDF using pdfplumber.
    Returns list of tables (each table is a list of rows).
    """
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                for table in page_tables:
                    # Clean table: replace None with empty string
                    clean_table = [
                        [cell if cell is not None else "" for cell in row]
                        for row in table
                    ]
                    tables.append(clean_table)
    return tables


def extract_text_lines(pdf_path):
    """
    Fallback: Extract structured text when no tables found.
    Returns structured data for non-tabular documents (CVs, reports, etc.).
    """
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            for line in text.splitlines():
                if line.strip():
                    lines.append([line])
    return [lines] if lines else []


def extract_structured_text_json(pdf_path):
    """
    Extract structured text content for JSON output (CVs, resumes, reports).
    Organizes content by pages and sections.
    """
    result = {
        "document_type": "text",
        "pages": []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            
            if not text.strip():
                continue
            
            # Split into lines and organize
            lines = [line for line in text.splitlines() if line.strip()]
            
            page_data = {
                "page_number": page_num,
                "line_count": len(lines),
                "content": text.strip(),
                "lines": lines
            }
            
            result["pages"].append(page_data)
    
    return result
