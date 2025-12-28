# Contributing

> Join the VlaamsCodex community! 🤝

Thank you for your interest in contributing to VlaamsCodex! This guide covers everything you need to get started.

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

---

## Getting Started

### Prerequisites

- **Python 3.10+** (required)
- **Git** for version control
- **Node.js 18+** (for VS Code extension development)

### Development Setup

1. **Fork and clone** the repository:

```bash
git clone https://github.com/your-username/vlaamscodex.git
cd vlaamscodex
```

2. **Create a virtual environment** and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

3. **Verify your setup**:

```bash
# Run tests
pytest tests/ -v

# Run a Platskript file
plats run examples/hello.plats

# Check the CLI
plats version
```

---

## How to Contribute

### Reporting Bugs

Before submitting a bug report:
- Check existing issues to avoid duplicates
- Verify the bug exists in the latest version

**When submitting a bug report, include:**

| Information | Example |
|-------------|---------|
| Python version | `3.11.4` |
| Operating system | `Ubuntu 22.04 / Windows 11 / macOS 14` |
| VlaamsCodex version | `0.2.0` |
| Steps to reproduce | Clear numbered steps |
| Expected behavior | What should happen |
| Actual behavior | What actually happens |
| Sample `.plats` code | Code that triggers the bug |
| Full error message | Complete traceback |

### Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the proposed feature
- Use case and motivation
- Example Platskript syntax (if applicable)
- Potential implementation approach

### Submitting Changes

1. **Create a feature branch**:

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** following the code style guidelines below

3. **Add or update tests** as needed

4. **Run the test suite**:

```bash
pytest tests/ -v
```

5. **Commit your changes** with a clear message:

```bash
git commit -m "Add feature: description of change"
```

6. **Push and create a pull request**

---

## Code Style

### Python

| Guideline | Example |
|-----------|---------|
| Python version | 3.10+ features are acceptable |
| Indentation | 4 spaces |
| Style guide | PEP 8 |
| Functions/variables | `snake_case` |
| Classes | `PascalCase` |
| Type hints | Required for public APIs |
| Private helpers | Prefix with `_` |

### Example

```python
from typing import Optional

def compile_statement(tokens: list[str]) -> Optional[str]:
    """Compile a single Platskript statement to Python.

    Args:
        tokens: List of parsed tokens from the statement.

    Returns:
        Python source code, or None if compilation fails.
    """
    if not tokens:
        return None

    # Implementation...
    return _translate_tokens(tokens)

def _translate_tokens(tokens: list[str]) -> str:
    """Internal helper for token translation."""
    # ...
```

### Platskript Extensions

When extending the language:

1. Keep keywords in Flemish dialect style
2. Document new syntax in `docs/04_language_spec.md`
3. Update `OP_MAP` in `compiler.py` for new operators
4. Maintain backward compatibility when possible

### Documentation

- Update relevant documentation when changing functionality
- Use clear, professional English
- Include code examples where helpful
- Maintain Flemish cultural flavor in user-facing docs

---

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

# Run with coverage
pytest tests/ --cov=src/vlaamscodex
```

### Writing Tests

| Guideline | Details |
|-----------|---------|
| Location | `tests/` directory |
| File naming | `test_*.py` |
| Function naming | `test_*` |
| Coverage | Both positive and negative test cases |
| Edge cases | Include boundary conditions |

### Test Example

```python
import pytest
from vlaamscodex.compiler import compile_plats

def test_compile_simple_print():
    """Test compiling a simple print statement."""
    plats = "klap tekst hello amen"
    result = compile_plats(plats)
    assert "print" in result
    assert "'hello'" in result

def test_compile_missing_amen_raises():
    """Test that missing amen raises syntax error."""
    plats = "klap tekst hello"
    with pytest.raises(SyntaxError):
        compile_plats(plats)
```

---

## Project Structure

```
src/vlaamscodex/
├── __init__.py      # Package metadata, version
├── cli.py           # Command-line interface, 80+ aliases
├── codec.py         # Source encoding codec
├── compiler.py      # Platskript transpiler
├── repl.py          # Interactive REPL
├── checker.py       # Syntax validation
├── examples.py      # Example browser
├── fortune.py       # Proverb easter egg
├── init.py          # Project scaffolding
└── dialects/        # Dialect transformer
    └── transformer.py
```

---

## Contribution Areas

### Language Development

**Adding new operators to Platskript:**

1. Add mapping to `OP_MAP` in `compiler.py`:

```python
OP_MAP = {
    # ... existing operators
    'nieuw_operator': 'python_op',
}
```

2. Update `docs/04_language_spec.md`
3. Add tests in `tests/test_compiler.py`

### CLI Development

**Adding new commands:**

1. Add aliases to `COMMAND_ALIASES` in `cli.py`
2. Create module following existing pattern:
   - `*_ALIASES` dict
   - `detect_*_dialect()` function
   - Main implementation
3. Wire into `main()` argparser
4. Add tests

### Dialect Packs

**Creating new dialect packs:**

1. Create JSON in `dialects/packs/`:

```json
{
  "id": "vlaams/newdialect",
  "label": "New Dialect",
  "inherits": ["vlaams/basis"],
  "protected_terms": [],
  "rules": []
}
```

2. Add entry to `dialects/index.json`
3. Run validation: `python tools/validate_dialect_packs.py`

**See:** [[Creating-Dialect-Packs]] for detailed guide.

### VS Code Extension

**Extension development:**

```bash
cd vscode-extension
npm install
npm run compile
# Press F5 in VS Code to debug
```

---

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass: `pytest tests/`
- [ ] Code follows style guidelines
- [ ] Documentation updated (if applicable)
- [ ] Dialect packs validated (if changed)
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Summary
Brief description of changes.

## Changes
- Change 1
- Change 2

## Testing
How were these changes tested?

## Related Issues
Fixes #123
```

---

## Development Tips

### Quick Iteration

```bash
# Install in editable mode
pip install -e .

# Test changes immediately
plats run examples/hello.plats

# Run specific test during development
pytest tests/test_compiler.py -v -x
```

### Debugging the Codec

```python
# Check codec registration
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"

# Test transpilation directly
from vlaamscodex.compiler import compile_plats
print(compile_plats("klap tekst hello amen"))
```

### Debugging Dialect Transformation

```python
from vlaamscodex.dialects.transformer import transform, available_packs

# List available packs
for pack in available_packs():
    print(f"{pack.id}: {pack.label}")

# Test transformation
result = transform("Gij hebt dat goed gedaan", "antwerps")
print(result)
```

---

## Release Process

Only maintainers can release, but here's how it works:

1. Update version in 3 locations:
   - `src/vlaamscodex/__init__.py`
   - `pyproject.toml`
   - `vscode-extension/package.json`

2. Update CHANGELOG

3. Create release commit:
   ```bash
   git commit -m "Release v0.x.x"
   git tag v0.x.x
   git push origin main --tags
   ```

4. CI builds and publishes to PyPI

**See:** [[Build-and-Release]] for detailed release documentation.

---

## Getting Help

### Resources

| Resource | Purpose |
|----------|---------|
| [[Architecture-Overview]] | Understand system design |
| [[Transpiler-Internals]] | Compiler details |
| [[Dialect-Engine]] | Transformer internals |
| [[Troubleshooting]] | Common issues |

### Contact

- **GitHub Issues**: Best for bug reports and feature requests
- **Pull Requests**: For code contributions
- **Discussions**: For questions and ideas

---

## Recognition

Contributors are recognized in:
- Git commit history
- GitHub contributor list
- Release notes (for significant contributions)

---

## See Also

- [[Architecture-Overview]] - System design
- [[Transpiler-Internals]] - Compiler details
- [[Dialect-Engine]] - Transformer internals
- [[Creating-Dialect-Packs]] - Create new dialects
- [[Build-and-Release]] - Build system

---

**Bedankt voor uw bijdrage!** 🧇
