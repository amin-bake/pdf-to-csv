# PDF to CSV Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A simple, user-friendly web application that converts PDF files to CSV format by extracting tables and text content. Built with Flask and pdfplumber, it supports batch processing and provides an intuitive drag-and-drop interface.

## ✨ Features

- 📤 **Multiple File Upload**: Drag & drop or select multiple PDF files at once
- 📊 **Smart Table Extraction**: Automatically detects and extracts tables from PDFs
- 🔄 **Automatic Merging**: Combines all tables from each PDF into a single CSV file
- 📈 **Real-time Progress**: Visual progress bars for upload and conversion
- ⬇️ **Flexible Downloads**: Download files individually or all at once as a ZIP
- 🎯 **Dual Parser Support**: Choose between pdfplumber (default) or Tabula for better compatibility
- 💻 **Clean UI**: Simple, intuitive interface that works on desktop and mobile
- ⚡ **Background Processing**: Non-blocking conversion with status polling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- (Optional) Java Runtime Environment for Tabula parser

### Installation

1. **Clone the repository**

   ```powershell
   git clone https://github.com/YOUR_USERNAME/pdf-to-csv.git
   cd pdf-to-csv
   ```

2. **Create and activate virtual environment**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

### Running the Application

```powershell
python app.py
```

Then open your browser and navigate to **http://localhost:5000**

## 📖 Usage

1. **Upload Files**: Click "choose files" or drag & drop PDF files onto the upload area
2. **Select Parser**: Choose between pdfplumber (default) or Tabula
3. **Convert**: Click "Convert uploaded files" to start processing
4. **Download**: Use individual download buttons or "Download All" for a ZIP archive

### Parser Options

- **pdfplumber** (default): Works well with most PDFs, no additional dependencies
- **Tabula**: Better for complex table layouts, requires Java runtime

## 🏗️ Architecture

```
pdf-to-csv/
├── app.py                      # Flask backend with conversion logic
├── templates/
│   └── index.html             # Frontend UI with JavaScript
├── requirements.txt           # Python dependencies
├── tests/
│   ├── test_e2e.py           # End-to-end integration tests
│   ├── test_upload.py        # Upload functionality tests
│   ├── test_download_types.py # Download behavior tests
│   └── test_download_all.py  # Batch download tests
├── README.md                  # This file
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Contribution guidelines
└── .gitignore                # Git ignore patterns
```

### API Endpoints

- `GET /` - Serve the web interface
- `POST /upload` - Upload a single PDF file
- `POST /convert` - Start conversion for uploaded files
- `GET /status/<file_id>` - Poll conversion status
- `GET /download/<file_id>` - Download converted file(s)
- `POST /download_all` - Download all files as ZIP

## 🧪 Testing

Run the test suite to verify functionality:

```powershell
# End-to-end test
python test_e2e.py

# Upload test
python test_upload.py

# Download behavior test
python test_download_types.py

# Download all test
python test_download_all.py
```

## 🔧 Configuration

The application uses in-memory storage for uploaded files and temporary directories for converted files. For production use, consider:

- Using a production WSGI server (gunicorn, waitress)
- Implementing file cleanup mechanisms
- Adding authentication/authorization
- Setting up proper logging
- Configuring file size limits

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and test thoroughly
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to your branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF table extraction
- [Tabula](https://github.com/tabulapedia/tabula-py) - Alternative parser
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [pandas](https://pandas.pydata.org/) - Data manipulation

## 📧 Support

If you encounter any issues or have questions:

- Open an [issue](https://github.com/YOUR_USERNAME/pdf-to-csv/issues)
- Check existing issues for solutions
- Read the [Contributing Guidelines](CONTRIBUTING.md)

## 🗺️ Roadmap

Potential future enhancements:

- [ ] Support for more output formats (Excel, JSON)
- [ ] Advanced table detection options
- [ ] Batch processing queue for large files
- [ ] Cloud storage integration
- [ ] API authentication
- [ ] Docker containerization
- [ ] Persistent storage option

---

Made with ❤️ by Mohamed Ali
