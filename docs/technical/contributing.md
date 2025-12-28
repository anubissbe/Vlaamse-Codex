# Contributing to VlaamsCodex

> Guide for developers who want to contribute to the project.

## Quick Start

```bash
# Clone repository
git clone https://github.com/anubissbe/Vlaamse-Codex.git
cd Vlaamse-Codex

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Verify magic mode
python examples/hello.plats
```

## Development Workflow

### 1. Branch Strategy

```
main              # Stable, release-ready
  └── feature/*   # New features
  └── fix/*       # Bug fixes
  └── docs/*      # Documentation
```

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, commit
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/my-feature
```

### 2. Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new operator 'modulo'
fix: handle empty input in compiler
docs: update API reference
test: add coverage for checker module
refactor: simplify expression parsing
chore: update dependencies
```

### 3. Pull Request Process

1. Ensure tests pass: `pytest tests/ -v`
2. Update documentation if needed
3. Add/update tests for new code
4. Request review
5. Squash and merge

## Code Standards

### Python Style

- **Python 3.10+**: Use modern syntax (type hints, `|` union, etc.)
- **Formatting**: Follow PEP 8 (use `black` if available)
- **Type hints**: Required for public APIs
- **Docstrings**: Google style for public functions

```python
def compile_plats(plats_src: str) -> str:
    """Compile Platskript source to Python.

    Args:
        plats_src: Platskript source code.

    Returns:
        Generated Python source code.

    Raises:
        ValueError: If source has syntax errors.
    """
```

### File Organization

```python
# Module docstring first
"""Brief description of module."""

# Imports: stdlib, then third-party, then local
from __future__ import annotations

import re
from pathlib import Path

from .compiler import compile_plats

# Constants
OP_MAP = {...}

# Private helpers (underscore prefix)
def _helper_function():
    ...

# Public API
def public_function():
    ...
```

## Common Contribution Types

### Adding a New Operator

1. **Update `OP_MAP`** in `compiler.py`:
   ```python
   OP_MAP["modulo"] = "%"
   ```

2. **Add tests** in `test_compiler.py`:
   ```python
   def test_modulo_operator():
       plats = "plan doe\n  zet x op getal 10 modulo getal 3 amen\ngedaan"
       py = compile_plats(plats)
       assert "10 % 3" in py
   ```

3. **Update documentation** in `docs/04_language_spec.md`

### Adding a CLI Command

1. **Create command module** (e.g., `src/vlaamscodex/newcmd.py`):
   ```python
   """Description of new command."""

   NEWCMD_ALIASES = {
       "newcmd": "newcmd",
       "nieuwecommando": "west-vlaams",
   }

   def detect_newcmd_dialect(alias: str) -> str | None:
       return NEWCMD_ALIASES.get(alias)

   def newcmd_handler(args, dialect: str | None = None) -> int:
       # Implementation
       return 0
   ```

2. **Wire into CLI** in `cli.py`:
   ```python
   COMMAND_ALIASES.update({
       "newcmd": "newcmd",
       "nieuwecommando": "newcmd",
   })

   # In main():
   elif base_command == "newcmd":
       from .newcmd import newcmd_handler, detect_newcmd_dialect
       return newcmd_handler(args, detect_newcmd_dialect(args.command))
   ```

3. **Add argparser subcommand**

4. **Add tests and documentation**

### Creating a Dialect Pack

1. **Add entry to `dialects/index.json`**:
   ```json
   {
     "id": "nieuw-dialect",
     "label": "Nieuw Dialect",
     "file": "nieuw-dialect.json",
     "inherits": ["algemeen-vlaams"]
   }
   ```

2. **Create pack file** `dialects/packs/nieuw-dialect.json`:
   ```json
   {
     "id": "nieuw-dialect",
     "label": "Nieuw Dialect",
     "inherits": ["algemeen-vlaams"],
     "protected_terms": [],
     "rules": [
       {
         "type": "replace_word",
         "from": "gij",
         "to": "ge",
         "preserve_case": true
       }
     ]
   }
   ```

3. **Validate** with `python tools/validate_dialect_packs.py`

4. **Add tests** for key transformations

### Improving Documentation

1. **API docs**: `docs/api/<module>.md`
2. **Architecture**: `docs/architecture/`
3. **Technical**: `docs/technical/`
4. **User guide**: `docs/06_user_guide.md`

Always update `PROJECT_INDEX.json` and `PROJECT_INDEX.md` when adding docs.

## Project Structure

```
Vlaamse-Codex/
├── src/vlaamscodex/       # Main package
├── dialects/              # Dialect pack data
├── tests/                 # Test suite
├── examples/              # Sample programs
├── docs/                  # Documentation
│   ├── architecture/      # System design
│   ├── api/               # API reference
│   └── technical/         # Developer docs
├── tools/                 # Development utilities
├── vscode-extension/      # VS Code extension
├── pyproject.toml         # Package config
└── vlaamscodex_build_backend.py  # Custom build
```

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=vlaamscodex

# Stop on first failure
pytest tests/ -x

# Run specific test
pytest tests/test_compiler.py::test_compile_plats_hello_shape -v
```

### Writing Tests

```python
def test_descriptive_name():
    """Docstring explaining what's tested."""
    # Arrange
    input_data = "..."

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected
```

## Version Management

Version appears in three files (keep in sync):

1. `src/vlaamscodex/__init__.py`: `__version__ = "0.2.0"`
2. `pyproject.toml`: `version = "0.2.0"`
3. `vscode-extension/package.json`: `"version": "0.2.0"`

## Release Process

1. Update version in all three files
2. Update CHANGELOG.md
3. Create PR, merge to main
4. Tag release: `git tag v0.2.0 && git push --tags`
5. CI builds and publishes to PyPI

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/anubissbe/Vlaamse-Codex/issues)
- **Documentation**: Start with `CLAUDE.md` and `docs/`
- **Code questions**: Read existing similar code first

## License

MIT License - see LICENSE file. By contributing, you agree to license your work under MIT.
