"""
Conversion Worker Module
Background processing of PDF conversion jobs.
"""
import os
import threading
from datetime import datetime, timezone

from extractors import extract_tables_pdfplumber, extract_text_lines
from converters import save_tables_to_csv, save_tables_to_excel, save_tables_to_json, save_tables_to_text


class ConversionWorker:
    """Handles background processing of PDF conversion jobs."""
    
    def __init__(self, upload_folder, converted_folder, jobs_storage):
        """
        Initialize the conversion worker.
        
        Args:
            upload_folder: Path to uploaded PDF files
            converted_folder: Path for converted output files
            jobs_storage: Reference to shared jobs dictionary
        """
        self.upload_folder = upload_folder
        self.converted_folder = converted_folder
        self.jobs = jobs_storage
    
    def process_conversion(self, job_id, file_infos, parser, merge, output_format='csv'):
        """
        Process PDF conversion in background thread.
        Updates job status as it progresses.
        
        Args:
            job_id: Unique job identifier
            file_infos: List of file information dictionaries
            parser: Parser to use ('pdfplumber' or 'tabula')
            merge: Whether to merge tables into single file
            output_format: Output format ('csv', 'excel', 'json', 'text')
        """
        job = self.jobs[job_id]
        job['status'] = 'processing'
        job['progress'] = 0
        
        try:
            total_files = len(file_infos)
            all_converted = []
            
            for idx, file_info in enumerate(file_infos):
                file_id = file_info['fileId']
                filename = file_info['filename']
                
                # Find the PDF file
                pdf_path = self._find_pdf_file(file_id)
                
                if not pdf_path:
                    job['errors'].append(f"File not found: {filename}")
                    continue
                
                # Update status
                job['status'] = 'converting'
                job['currentFile'] = filename
                
                # Extract tables
                tables = self._extract_tables(pdf_path, parser)
                
                # Create output directory for this file
                base_filename = os.path.splitext(filename)[0]
                file_output_dir = os.path.join(self.converted_folder, job_id, file_id)
                os.makedirs(file_output_dir, exist_ok=True)
                
                # Convert to requested format
                converted_files = self._convert_to_format(
                    tables, file_output_dir, base_filename, 
                    merge, output_format, pdf_path
                )
                
                # Register converted files
                for file_path in converted_files:
                    file_info = {
                        'fileId': f"{file_id}_{os.path.basename(file_path)}",
                        'originalFileId': file_id,
                        'filename': os.path.basename(file_path),
                        'filepath': file_path,
                        'size': os.path.getsize(file_path)
                    }
                    all_converted.append(file_info)
                
                # Update progress
                job['progress'] = int(((idx + 1) / total_files) * 100)
            
            # Mark as completed
            job['status'] = 'completed'
            job['progress'] = 100
            job['convertedFiles'] = all_converted
            job['completedAt'] = datetime.now(timezone.utc).isoformat(),
            job['message'] = f"Successfully converted {len(all_converted)} file(s)"
            
        except Exception as e:
            job['status'] = 'error'
            job['progress'] = 100
            job['error'] = str(e)
            job['message'] = f"Conversion failed: {str(e)}"
    
    def start_conversion(self, file_ids, parser, merge, output_format='csv'):
        """
        Start conversion in background thread.
        
        Args:
            file_ids: List of file IDs to convert
            parser: Parser to use
            merge: Whether to merge tables
            output_format: Output format
            
        Returns:
            job_id: String identifier for the job
        """
        import uuid
        
        # Generate job ID
        job_id = uuid.uuid4().hex
        
        # Build file info list
        file_infos = []
        for file_id in file_ids:
            file_infos.append({
                'fileId': file_id,
                'filename': f"{file_id}.pdf"  # Will be updated when file is found
            })
        
        # Create job entry
        self.jobs[job_id] = {
            'jobId': job_id,
            'status': 'pending',
            'progress': 0,
            'fileIds': file_ids,
            'parser': parser,
            'merge': merge,
            'outputFormat': output_format,
            'createdAt': datetime.now(timezone.utc).isoformat(),
            'currentFile': None,
            'convertedFiles': [],
            'errors': [],
            'error': None,
            'message': 'Conversion queued'
        }
        
        # Start background thread
        thread = threading.Thread(
            target=self.process_conversion,
            args=(job_id, file_infos, parser, merge, output_format),
            daemon=True
        )
        thread.start()
        
        return job_id
    
    def _find_pdf_file(self, file_id):
        """Find PDF file by ID in upload folder."""
        for filename in os.listdir(self.upload_folder):
            if filename.startswith(file_id):
                pdf_path = os.path.join(self.upload_folder, filename)
                if os.path.exists(pdf_path):
                    return pdf_path
        return None
    
    def _extract_tables(self, pdf_path, parser):
        """
        Extract tables from PDF using specified parser.
        
        Args:
            pdf_path: Path to PDF file
            parser: Parser to use ('pdfplumber' or 'tabula')
            
        Returns:
            List of extracted tables
        """
        if parser == 'pdfplumber':
            tables = extract_tables_pdfplumber(pdf_path)
            
            # Fallback to text if no tables found
            if not tables:
                tables = extract_text_lines(pdf_path)
        else:
            # Future: Add tabula support
            # For now, fall back to pdfplumber
            tables = extract_tables_pdfplumber(pdf_path)
        
        return tables
    
    def _convert_to_format(self, tables, output_dir, base_filename, 
                          merge, output_format, pdf_path=None):
        """
        Convert tables to requested output format.
        
        Args:
            tables: Extracted tables
            output_dir: Output directory path
            base_filename: Base filename for output
            merge: Whether to merge tables
            output_format: Output format ('csv', 'excel', 'json', 'text')
            pdf_path: Path to original PDF (for JSON/text extraction fallback)
            
        Returns:
            List of converted file paths
        """
        # For JSON and text formats, always call save function as they handle text extraction fallback
        if output_format == 'json':
            return save_tables_to_json(
                tables, output_dir, base_filename, merge, pdf_path
            )
        elif output_format == 'text':
            return save_tables_to_text(
                tables, output_dir, base_filename, merge, pdf_path
            )
        elif tables:
            # CSV and Excel only process when tables exist
            if output_format == 'excel':
                return save_tables_to_excel(
                    tables, output_dir, base_filename, merge
                )
            else:  # CSV
                return save_tables_to_csv(
                    tables, output_dir, base_filename, merge
                )
        else:
            # No tables and not JSON/text format - return empty list
            return []
