"""
Table Analysis Module
Intelligent analysis of table structures to identify headers, titles, and data rows.
"""


def clean_header(header):
    """Clean and normalize header text."""
    if not header or not str(header).strip():
        return None
    # Remove newlines and extra whitespace
    cleaned = str(header).replace('\n', ' ').strip()
    # Remove multiple spaces
    cleaned = ' '.join(cleaned.split())
    return cleaned if cleaned else None


def is_title_row(row):
    """
    Detect if a row is likely a title/header row rather than column headers.
    Title rows typically have:
    1. Only one or two cells with content (rest are empty)
    2. Longer text that spans conceptually across the table
    3. No data-like patterns (numbers, codes, structured text)
    """
    non_empty_cells = [cell for cell in row if cell and str(cell).strip()]
    
    # If most cells are empty, likely a title
    if len(non_empty_cells) <= 2 and len(row) > 3:
        # Check if the non-empty content is longer text (likely a title)
        for cell in non_empty_cells:
            cell_text = str(cell).strip()
            # Titles are usually longer and contain spaces or newlines
            if len(cell_text) > 15 or '\n' in str(cell):
                return True
    
    return False


def analyze_table_structure(table):
    """
    Intelligently analyze table structure to identify:
    - Title rows
    - Header rows
    - Data rows
    - Empty/separator rows
    Returns structured information about the table.
    """
    if not table or len(table) < 2:
        return None
    
    structure = {
        'title_rows': [],
        'header_row_idx': None,
        'data_start_idx': None,
        'column_count': 0,
        'has_sequential_ids': False
    }
    
    # Analyze each row
    row_analysis = []
    for idx, row in enumerate(table):
        analysis = {
            'idx': idx,
            'type': 'unknown',
            'non_empty_count': 0,
            'numeric_count': 0,
            'text_count': 0,
            'long_text_count': 0,
            'barcode_count': 0,
            'short_number_count': 0,
            'is_empty': False,
            'cells': []
        }
        
        for cell in row:
            cell_str = str(cell).strip() if cell else ""
            analysis['cells'].append(cell_str)
            
            if not cell_str:
                continue
            
            analysis['non_empty_count'] += 1
            
            # Check cell characteristics
            if cell_str.isdigit():
                analysis['numeric_count'] += 1
                # Long numbers might be barcodes (data)
                if len(cell_str) > 8:
                    analysis['barcode_count'] += 1
                # Short numbers (1-3 digits) might be IDs or quantities (data)
                elif len(cell_str) <= 3:
                    analysis['short_number_count'] += 1
            elif any(c.isalpha() for c in cell_str):
                analysis['text_count'] += 1
                if len(cell_str) > 20 or '\n' in cell_str:
                    analysis['long_text_count'] += 1
        
        # Classify row type
        if analysis['non_empty_count'] == 0:
            analysis['type'] = 'empty'
            analysis['is_empty'] = True
        elif analysis['non_empty_count'] <= 2 and len(row) > 3 and analysis['long_text_count'] > 0:
            analysis['type'] = 'title'
        else:
            # Determine if it's a header or data row
            analysis['type'] = 'unknown'
        
        row_analysis.append(analysis)
    
    # Find title rows (at the beginning)
    for analysis in row_analysis:
        if analysis['type'] == 'title':
            structure['title_rows'].append(analysis)
        elif analysis['type'] != 'empty':
            break  # Stop at first non-title, non-empty row
    
    # Find header row using keyword scoring
    header_candidates = []
    header_keywords = [
        'sno', 's.no', 'no', 'serial', 'number', '#', 'name', 'description', 
        'price', 'code', 'barcode', 'bar code', 'brand', 'item', 
        'product', 'quantity', 'qty', 'amount', 'date', 'time', 
        'category', 'type', 'status', 'id', 'image', 'wholesale', 
        'retail', 'ml', 'pcs', 'ctn', 'carton', 'pieces', 'count',
        'total', 'subtotal', 'unit', 'size', 'color', 'model', 'sku'
    ]
    
    for analysis in row_analysis:
        if analysis['type'] in ['title', 'empty']:
            continue
        
        score = 0
        is_likely_data = False
        
        # Check each cell for header vs data characteristics
        for cell in analysis['cells'][:8]:  # Check first 8 columns
            if not cell:
                continue
            
            cell_lower = cell.lower().strip()
            
            # Strong indicators this is a HEADER row
            if any(keyword == cell_lower or keyword in cell_lower for keyword in header_keywords):
                score += 5  # Strong header signal
            
            # Check for typical header patterns
            if any(c.isalpha() for c in cell) and len(cell) >= 2 and len(cell) <= 30:
                # Contains letters, reasonable length for a header
                if not cell.isdigit() and not (len(cell) > 8 and cell.replace('.', '').replace(',', '').isdigit()):
                    score += 2
            
            # Strong indicators this is a DATA row (not header)
            # 1. Long numeric codes (barcodes)
            if cell.isdigit() and len(cell) > 8:
                is_likely_data = True
                score -= 10
            
            # 2. Currency values
            if 'ksh' in cell_lower or '$' in cell or '€' in cell or '£' in cell:
                if any(c.isdigit() for c in cell):
                    is_likely_data = True
                    score -= 8
            
            # 3. Single digit numbers (likely IDs in data rows)
            if cell.isdigit() and len(cell) == 1:
                score -= 3
            
            # 4. Product-like descriptions with specific details
            if '(' in cell and ')' in cell and len(cell) > 15:
                # Like "Ameer Al Arab (Black) Edp" - likely data
                score -= 2
        
        # Don't consider rows with clear data indicators as headers
        if not is_likely_data and score > 0:
            header_candidates.append((analysis['idx'], score, analysis))
    
    # Select best header candidate
    if header_candidates:
        header_candidates.sort(key=lambda x: x[1], reverse=True)
        best_score = header_candidates[0][1]
        
        if best_score >= 6:  # Increased threshold for confidence
            structure['header_row_idx'] = header_candidates[0][0]
            structure['data_start_idx'] = header_candidates[0][0] + 1
    
    # If still no header found, look for patterns
    if structure['header_row_idx'] is None:
        # Find first row after titles that has text but minimal barcodes/numbers
        for analysis in row_analysis:
            if analysis['type'] in ['title', 'empty']:
                continue
            
            # Headers typically have more text than pure numbers/barcodes
            if (analysis['text_count'] >= 3 and 
                analysis['barcode_count'] == 0 and
                analysis['short_number_count'] <= 1):
                structure['header_row_idx'] = analysis['idx']
                structure['data_start_idx'] = analysis['idx'] + 1
                break
    
    # Last resort: use first non-title row
    if structure['header_row_idx'] is None:
        for analysis in row_analysis:
            if analysis['type'] not in ['title', 'empty']:
                structure['header_row_idx'] = analysis['idx']
                structure['data_start_idx'] = analysis['idx'] + 1
                break
    
    # Determine column count
    structure['column_count'] = max(len(row) for row in table) if table else 0
    
    # Check if data has sequential IDs in first column
    if structure['data_start_idx'] and structure['data_start_idx'] < len(table):
        first_col_values = []
        for idx in range(structure['data_start_idx'], min(structure['data_start_idx'] + 5, len(table))):
            if idx < len(table) and len(table[idx]) > 0:
                val = str(table[idx][0]).strip()
                if val.isdigit():
                    first_col_values.append(int(val))
        
        # Check if sequential
        if len(first_col_values) >= 3:
            if first_col_values == list(range(first_col_values[0], first_col_values[0] + len(first_col_values))):
                structure['has_sequential_ids'] = True
    
    return structure


def create_headers(row, col_count, structure=None):
    """Create clean, unique headers from a row with intelligent naming."""
    headers = []
    seen = {}
    
    for col_idx in range(col_count):
        header = clean_header(row[col_idx]) if col_idx < len(row) else None
        
        if not header:
            # Generate intelligent column names based on position
            if col_idx == 0 and structure and structure.get('has_sequential_ids'):
                header = "id"
            else:
                header = f"column_{col_idx + 1}"
        else:
            # Ensure uniqueness by adding suffix if needed
            original = header
            counter = 1
            while header in seen:
                header = f"{original}_{counter}"
                counter += 1
            seen[header] = True
        
        headers.append(header)
    return headers


def validate_table_data(tables):
    """
    Check if extracted data is truly tabular or just poorly parsed text.
    Returns True if data appears to be valid tables.
    """
    for table in tables:
        if len(table) >= 3:  # At least 3 rows
            # Check column count consistency
            col_counts = [len(row) for row in table]
            max_cols = max(col_counts) if col_counts else 0
            
            # If most rows have multiple columns and structure is consistent
            if max_cols >= 3:
                # Check if at least 70% of rows have 2+ columns
                multi_col_rows = sum(1 for count in col_counts if count >= 2)
                if multi_col_rows / len(table) >= 0.7:
                    return True
    
    return False
