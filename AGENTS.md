# Agent Guidelines

Guidelines for AI coding agents working with the VlaamsCodex repository.

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `src/vlaamscodex/` | Core implementation (compiler, codec, CLI) |
| `examples/` | Sample Platskript programs |
| `docs/` | Technical documentation and specifications |
| `data/` | Runtime artifacts (`.pth` startup hook) |
| `tests/` | Test suite |

**Note**: `pyproject.toml.example` is a reference template, not active configuration.

## Development Commands

| Command | Description |
|---------|-------------|
| `plats run examples/hello.plats` | Execute a Platskript program |
| `plats build examples/hello.plats --out /tmp/hello.py` | Compile to Python file |
| `plats show-python examples/hello.plats` | Display generated Python source |
| `python -m build` | Build sdist and wheel distributions |
| `pytest tests/` | Run test suite |

## Code Style

- **Python Version**: 3.10+ (see `pyproject.toml`)
- **Module Design**: Single-purpose modules (`codec.py`, `compiler.py`, `cli.py`)
- **Indentation**: 4 spaces
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes
- **Type Hints**: Required for public APIs; prefix private helpers with `_`

## Testing

Test suite located in `tests/` using pytest.

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_compiler.py -v

# Run specific test function
pytest tests/test_compiler.py::test_compile_plats_hello_shape -v
```

## Commit Guidelines

- Include concise summary describing the change
- For bug fixes: include reproduction steps and sample `.plats` input/output
- Reference related issues when applicable

## Security Considerations

- Treat `.plats` files as executable code
- Never execute untrusted Platskript files automatically
- The `.pth` startup hook executes during Python initialization; ensure it remains minimal
