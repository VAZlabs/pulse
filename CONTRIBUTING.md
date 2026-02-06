# Contributing to pulse

Thank you for your interest in contributing to pulse! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check if the issue already exists. When creating a bug report, include:

1. **Environment**: OS, Python version, how you installed pulse
2. **Steps to reproduce**: Clear steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Error logs**: Full error messages and traceback

Example:
```
Title: DNS check fails on Alpine Linux

Environment:
- OS: Alpine Linux 3.15
- Python: 3.9
- Installation: From source

Steps:
1. Run: python pulse.py api.github.com
2. Observe DNS check fails with "socket.gaierror"

Expected: DNS resolution should work
Actual: Fails with socket error

Error:
socket.gaierror: [Errno -2] Name or service not known
```

### Suggesting Enhancements

Suggestions for improvements are welcome! Include:

1. **Use case**: Why would this be useful?
2. **Proposed solution**: How should it work?
3. **Alternative solutions**: Other approaches you've considered
4. **Examples**: Usage examples if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests and linting: `make test`
6. Commit with descriptive messages
7. Push to your fork
8. Create a Pull Request with description

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourname/pulse.git
cd pulse

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
python -m pytest test_pulse.py -v

# Run linting
black pulse.py
pylint pulse.py
```

## Code Style

### Python Style Guide (PEP 8)

- Use 4 spaces for indentation
- Line length max 120 characters
- Meaningful variable names
- Add docstrings to functions and classes

### Code Formatting

Format code with black:
```bash
black pulse.py
```

### Linting

Check code quality with pylint:
```bash
pylint pulse.py
```

### Type Hints

Add type hints where possible:
```python
def check_dns(host: str) -> Tuple[Optional[str], float, Optional[Exception]]:
    """Resolve hostname to IP address"""
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest test_pulse.py -v

# Run specific test
python -m pytest test_pulse.py::TestDNSCheck -v

# Run with coverage
python -m pytest test_pulse.py --cov=pulse
```

### Writing Tests

```python
import unittest
from pulse import check_dns

class TestMyFeature(unittest.TestCase):
    def test_valid_case(self):
        """Test valid input"""
        result = check_dns("localhost")
        self.assertIsNotNone(result)
    
    def test_invalid_case(self):
        """Test invalid input"""
        result = check_dns("invalid.invalid.invalid")
        self.assertIsNone(result)
```

## Documentation

### Updating README

- Keep README.md up-to-date with new features
- Include usage examples
- Update feature list if adding new capabilities

### Adding Documentation

- Place new docs in root directory (e.g., TROUBLESHOOTING.md)
- Use clear, concise language
- Include examples where helpful

### Docstrings

Add docstrings to all functions and classes:

```python
def check_http(host: str, port: int, use_tls: bool = True) -> Tuple[float, Optional[int]]:
    """
    Make HTTP GET request to /health endpoint
    
    Args:
        host: Target hostname or IP
        port: Target port number
        use_tls: Whether to use HTTPS (default: True)
    
    Returns:
        Tuple of (duration_ms, status_code)
    
    Raises:
        socket.error: If connection fails
        ssl.SSLError: If TLS handshake fails
    """
    pass
```

## Commit Messages

Write clear, descriptive commit messages:

```
# Good
feat: Add HTTP timeout parameter
- Adds --timeout flag to control individual check timeouts
- Defaults to 10 seconds
- Useful for slow networks

# Bad
fix bug
update code
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build, dependencies, tooling

## Review Process

1. All PRs require review by maintainers
2. Automated tests must pass
3. Code style checks must pass
4. At least one approval required before merge

## Areas for Contribution

### High Priority

- [ ] Windows support improvements
- [ ] Additional test coverage
- [ ] Performance optimizations
- [ ] Documentation improvements

### Medium Priority

- [ ] Support for HTTP/2
- [ ] Custom health check endpoints
- [ ] Configuration file support
- [ ] Colored output on Windows

### Low Priority

- [ ] GUI application
- [ ] Web dashboard
- [ ] Integration with cloud monitoring services

## Release Process

Maintainers will:

1. Update version in `setup.py`
2. Update CHANGELOG
3. Tag release: `git tag v1.0.0`
4. Build distribution: `python setup.py sdist bdist_wheel`
5. Upload to PyPI: `twine upload dist/*`

## Questions?

- Check existing issues and documentation first
- Ask in discussions/issues for clarification
- Email maintainers if needed

Thank you for contributing to pulse! 🎉
