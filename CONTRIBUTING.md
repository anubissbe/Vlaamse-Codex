# Contributing to VlaamsCodex

Thank you for your interest in contributing to VlaamsCodex! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## Getting Started

### Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/vlaamscodex.git
   cd vlaamscodex
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Verify your setup:
   ```bash
   pytest tests/
   plats run examples/hello.plats
   ```

## How to Contribute

### Reporting Bugs

Before submitting a bug report:
- Check existing issues to avoid duplicates
- Verify the bug exists in the latest version

When submitting a bug report, include:
- Python version and operating system
- Steps to reproduce the issue
- Expected vs. actual behavior
- Sample `.plats` code that triggers the bug
- Full error message/traceback

### Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the proposed feature
- Use case and motivation
- Example Platskript syntax (if applicable)

### Submitting Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines below

3. Add or update tests as needed

4. Run the test suite:
   ```bash
   pytest tests/
   ```

5. Commit your changes with a clear message:
   ```bash
   git commit -m "Add feature: description of change"
   ```

6. Push and create a pull request

## Code Style

### Python

- Python 3.10+ features are acceptable
- Use 4-space indentation
- Follow PEP 8 conventions
- Use `snake_case` for functions and variables
- Use `PascalCase` for classes
- Add type hints to public APIs
- Prefix private helpers with `_`

### Platskript

When extending the language:
- Keep keywords in Flemish dialect style
- Document new syntax in `docs/04_language_spec.md`
- Update `OP_MAP` in `compiler.py` for new operators
- Maintain backward compatibility when possible

### Documentation

- Update relevant documentation when changing functionality
- Use clear, professional English
- Include code examples where helpful

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_compiler.py

# Run specific test
pytest tests/test_compiler.py::test_compile_plats_hello_shape
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Include both positive and negative test cases
- Test edge cases and error conditions

## Project Structure

```
src/vlaamscodex/
├── __init__.py      # Package metadata
├── cli.py           # Command-line interface
├── codec.py         # Source encoding codec
└── compiler.py      # Platskript transpiler
```

## Questions?

If you have questions about contributing, feel free to open an issue for discussion.
