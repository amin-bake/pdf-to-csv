# Contributing to PDF to CSV

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, browser)

### Suggesting Enhancements

We welcome feature requests! Please open an issue with:

- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, descriptive commits
3. **Test your changes** - ensure all existing tests pass and add new tests if needed
4. **Update documentation** - update README.md if you've changed functionality
5. **Submit a pull request** with a clear description of your changes

#### Development Setup

```powershell
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pdf-to-csv.git
cd pdf-to-csv

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run the application
python app.py
```

#### Running Tests

```powershell
# Run individual test files
python test_e2e.py
python test_upload.py
python test_download_types.py
python test_download_all.py
```

### Code Style

- Follow PEP 8 guidelines for Python code
- Use clear, descriptive variable and function names
- Add comments for complex logic
- Keep functions focused and modular

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (e.g., "Add", "Fix", "Update", "Remove")
- Keep the first line under 50 characters
- Add detailed description if needed

Example:

```
Add support for custom output formats

- Implement JSON export option
- Add configuration for delimiter choice
- Update documentation with new examples
```

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment, discrimination, or derogatory comments
- Trolling or deliberately inflammatory comments
- Publishing others' private information
- Other conduct that could reasonably be considered inappropriate

## Questions?

Feel free to open an issue with the "question" label if you need help or clarification on anything.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
