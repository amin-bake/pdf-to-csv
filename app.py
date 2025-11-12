import io
import csv
import zipfile
import threading
import uuid
import json
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
import pdfplumber
import os
import tempfile
import pandas as pd

# Optional tabula import; tabula-py requires Java on the system. We import lazily below.
try:
    import tabula
    _HAS_TABULA = True
except Exception:
    tabula = None
    _HAS_TABULA = False

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory store for uploaded files and statuses. Keys are file IDs (uuid hex).
uploaded_files = {}


def _save_uploaded_file_storage(file_storage):
    """Save uploaded FileStorage to a temp file and register it in uploaded_files.
    Returns the generated file id."""
    file_id = uuid.uuid4().hex
    fd, path = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    file_storage.save(path)
    uploaded_files[file_id] = {
        'id': file_id,
        'name': file_storage.filename,
        'path': path,
        'status': 'uploaded',
        'progress': 0,
        'converted_files': [],
        'error': None,
    }
    return file_id


@app.route('/')
def index():
    return render_template('index.html')


def tables_from_pdf_bytes(pdf_bytes):
    """Return a list of tables (each table is list-of-rows) extracted from the PDF bytes."""
    tables = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            # extract_tables returns list of tables (each table as list of rows)
            page_tables = page.extract_tables()
            if page_tables:
                for t in page_tables:
                    # Clean table: replace None with empty string
                    clean = [[cell if cell is not None else "" for cell in row] for row in t]
                    tables.append(clean)
    return tables


def convert_file(file_id, parser='pdfplumber', merge_tables=False):
    info = uploaded_files.get(file_id)
    if not info:
        return
    info['status'] = 'converting'
    info['progress'] = 0
    pdf_path = info['path']
    name_root = os.path.splitext(os.path.basename(info['name']))[0]
    out_dir = tempfile.mkdtemp(prefix=f"conv_{file_id}_")
    converted = []
    try:
        if parser == 'tabula' and _HAS_TABULA:
            # tabula-py uses file path
            try:
                dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
                if not dfs:
                    info['error'] = 'Tabula detected no tables'
                else:
                    if merge_tables:
                        df_all = pd.concat(dfs, ignore_index=True)
                        out_path = os.path.join(out_dir, f"{name_root}.csv")
                        df_all.to_csv(out_path, index=False)
                        converted.append(out_path)
                    else:
                        for idx, df in enumerate(dfs, start=1):
                            out_path = os.path.join(out_dir, f"{name_root}_table{idx}.csv")
                            df.to_csv(out_path, index=False)
                            converted.append(out_path)
                info['progress'] = 100
            except Exception as e:
                info['error'] = f"Tabula failed: {e}"
                info['progress'] = 100
        else:
            # pdfplumber path: iterate pages and update progress
            with pdfplumber.open(pdf_path) as pdf:
                total = max(1, len(pdf.pages))
                all_tables = []
                for i, page in enumerate(pdf.pages, start=1):
                    page_tables = page.extract_tables()
                    if page_tables:
                        for t in page_tables:
                            clean = [[cell if cell is not None else "" for cell in row] for row in t]
                            all_tables.append(clean)
                    # update progress per page
                    info['progress'] = int(i * 100 / total)

                if not all_tables:
                    # fallback to text lines
                    lines = []
                    for page in pdf.pages:
                        text = page.extract_text() or ''
                        for line in text.splitlines():
                            lines.append([line])
                    out_path = os.path.join(out_dir, f"{name_root}.csv")
                    with open(out_path, 'w', newline='', encoding='utf-8') as fh:
                        writer = csv.writer(fh)
                        writer.writerows(lines)
                    converted.append(out_path)
                else:
                    if merge_tables:
                        out_path = os.path.join(out_dir, f"{name_root}.csv")
                        with open(out_path, 'w', newline='', encoding='utf-8') as fh:
                            writer = csv.writer(fh)
                            for table in all_tables:
                                for row in table:
                                    writer.writerow(row)
                        converted.append(out_path)
                    else:
                        for idx, table in enumerate(all_tables, start=1):
                            out_path = os.path.join(out_dir, f"{name_root}_table{idx}.csv")
                            with open(out_path, 'w', newline='', encoding='utf-8') as fh:
                                writer = csv.writer(fh)
                                for row in table:
                                    writer.writerow(row)
                            converted.append(out_path)
                info['progress'] = 100

        info['converted_files'] = converted
        info['status'] = 'done' if not info.get('error') else 'error'
    except Exception as e:
        info['error'] = str(e)
        info['status'] = 'error'
        info['progress'] = 100


def start_conversion_background(file_ids, parser='pdfplumber', merge_tables=False):
    threads = []
    for fid in file_ids:
        # mark queued
        if fid in uploaded_files:
            uploaded_files[fid]['status'] = 'queued'
            t = threading.Thread(target=convert_file, args=(fid, parser, merge_tables), daemon=True)
            t.start()
            threads.append(t)
    return threads


@app.route('/upload', methods=['POST'])
def upload():
    # Single-file upload handler used by frontend (XHR with progress)
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'no file provided'}), 400
    fid = _save_uploaded_file_storage(f)
    return jsonify({'id': fid, 'name': uploaded_files[fid]['name']})


@app.route('/convert', methods=['POST'])
def convert():
    # This endpoint now acts as a trigger that starts background conversion for uploaded file IDs.
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Expected JSON body with file_ids, parser and merge options.'}), 400
    file_ids = data.get('file_ids', [])
    parser = data.get('parser', 'pdfplumber')
    merge = bool(data.get('merge', False))

    # Start background threads for conversion; return immediately so client can poll statuses.
    start_conversion_background(file_ids, parser=parser, merge_tables=merge)
    return jsonify({'started': True, 'file_ids': file_ids})


@app.route('/status/<file_id>', methods=['GET'])
def status(file_id):
    info = uploaded_files.get(file_id)
    if not info:
        return jsonify({'error': 'not found'}), 404
    return jsonify({
        'id': info['id'],
        'name': info['name'],
        'status': info['status'],
        'progress': info.get('progress', 0),
        'converted_files': [os.path.basename(p) for p in info.get('converted_files', [])],
        'error': info.get('error')
    })


@app.route('/download/<file_id>', methods=['GET'])
def download(file_id):
    info = uploaded_files.get(file_id)
    if not info:
        return 'not found', 404
    if not info.get('converted_files'):
        return 'no converted files for this id', 404

    converted_files = info['converted_files']
    
    # If only one file, return it directly as CSV
    if len(converted_files) == 1:
        file_path = converted_files[0]
        try:
            # Sanitize filename for download
            safe_name = os.path.basename(info['name']).replace('/', '_').replace('\\', '_')
            csv_filename = f"{os.path.splitext(safe_name)[0]}.csv"
            
            return send_file(
                file_path,
                mimetype='text/csv',
                as_attachment=True,
                download_name=csv_filename
            )
        except FileNotFoundError:
            return 'converted file not found (may have been cleaned up)', 404
    
    # Multiple files: return as ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for p in converted_files:
            # p may be absolute path
            arcname = os.path.basename(p)
            try:
                with open(p, 'rb') as fh:
                    zf.writestr(arcname, fh.read())
            except FileNotFoundError:
                # If temp file was deleted, add an error note instead
                zf.writestr(f"{arcname}_MISSING.txt", f"File {arcname} was not found (may have been cleaned up)")

    zip_buffer.seek(0)
    # Sanitize filename for download (remove path separators and special chars)
    safe_name = os.path.basename(info['name']).replace('/', '_').replace('\\', '_')
    download_filename = f"{os.path.splitext(safe_name)[0]}_csvs.zip"
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name=download_filename)


@app.route('/download_all', methods=['POST'])
def download_all():
    """Download all converted files from multiple file IDs as a single ZIP."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Expected JSON body with file_ids'}), 400
    
    file_ids = data.get('file_ids', [])
    if not file_ids:
        return jsonify({'error': 'No file IDs provided'}), 400
    
    # Collect all converted files from all file IDs
    all_files = []
    for file_id in file_ids:
        info = uploaded_files.get(file_id)
        if info and info.get('converted_files'):
            for file_path in info['converted_files']:
                all_files.append({
                    'path': file_path,
                    'original_name': info['name']
                })
    
    if not all_files:
        return jsonify({'error': 'No converted files available'}), 404
    
    # Create a ZIP with all files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for file_info in all_files:
            file_path = file_info['path']
            # Use basename for the archive name to avoid directory structure
            arcname = os.path.basename(file_path)
            try:
                with open(file_path, 'rb') as fh:
                    zf.writestr(arcname, fh.read())
            except FileNotFoundError:
                # If temp file was deleted, add an error note
                zf.writestr(f"{arcname}_MISSING.txt", 
                           f"File {arcname} was not found (may have been cleaned up)")
    
    zip_buffer.seek(0)
    download_filename = "converted_files.zip"
    return send_file(
        zip_buffer, 
        mimetype='application/zip', 
        as_attachment=True, 
        download_name=download_filename
    )


if __name__ == '__main__':
    # For local development only
    app.run(host='0.0.0.0', port=5000, debug=True)
