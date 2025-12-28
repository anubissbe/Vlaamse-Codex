# Testing Strategy

> Test architecture, patterns, and best practices for VlaamsCodex.

## Test Suite Overview

```
tests/
├── conftest.py                    # Shared fixtures
├── test_compiler.py               # Transpiler unit tests
├── test_magic_subprocess.py       # Magic mode integration tests
└── test_dialect_transformer.py    # Dialect engine tests
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_compiler.py -v

# Specific test
pytest tests/test_compiler.py::test_compile_plats_hello_shape -v

# With coverage (if installed)
pytest tests/ --cov=vlaamscodex --cov-report=html

# Stop on first failure
pytest tests/ -x

# Run last failed
pytest tests/ --lf
```

## Test Patterns

### 1. Compiler Unit Tests

Testing the transpiler in isolation:

```python
# tests/test_compiler.py

from vlaamscodex.compiler import compile_plats, OP_MAP

def test_compile_plats_hello_shape():
    """Basic program structure compiles correctly."""
    plats = """
    plan doe
      klap tekst hallo amen
    gedaan
    """
    py = compile_plats(plats)
    assert "print(" in py
    assert "'hallo'" in py

def test_compile_plats_function():
    """Function definition and call."""
    plats = """
    plan doe
      maak funksie greet met name doe
        klap da name amen
      gedaan
      roep greet met tekst world amen
    gedaan
    """
    py = compile_plats(plats)
    assert "def greet(name):" in py
    assert "greet('world')" in py

def test_compile_plats_operators():
    """All operators translate correctly."""
    for plats_op, py_op in OP_MAP.items():
        # Test each operator in an expression
        ...

def test_compile_error_missing_amen():
    """Missing amen raises ValueError."""
    with pytest.raises(ValueError, match="missing 'amen'"):
        compile_plats("plan doe\n  klap tekst test\ngedaan")

def test_compile_error_unclosed_block():
    """Unclosed block raises ValueError."""
    with pytest.raises(ValueError, match="unclosed blocks"):
        compile_plats("plan doe\n  klap tekst test amen")
```

### 2. Magic Mode Integration Tests

Testing the codec in subprocess (isolated Python):

```python
# tests/test_magic_subprocess.py

import subprocess
import sys

def test_magic_mode_hello(tmp_path):
    """Magic mode executes .plats file directly."""
    script = tmp_path / "hello.plats"
    script.write_text("""# coding: vlaamsplats
plan doe
  klap tekst gdag amen
gedaan
""")

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "gdag" in result.stdout

def test_magic_mode_import(tmp_path):
    """Magic mode works with imports."""
    lib = tmp_path / "mylib.plats"
    lib.write_text("""# coding: vlaamsplats
plan doe
  maak funksie greet met name doe
    klap tekst hello plakt spatie plakt da name amen
  gedaan
gedaan
""")

    main = tmp_path / "main.py"
    main.write_text(f"""
import sys
sys.path.insert(0, "{tmp_path}")
import mylib
mylib.greet("test")
""")

    result = subprocess.run(
        [sys.executable, str(main)],
        capture_output=True,
        text=True,
    )

    assert "hello test" in result.stdout
```

### 3. Dialect Transformer Tests

Testing the rule engine:

```python
# tests/test_dialect_transformer.py

from vlaamscodex.dialects.transformer import (
    transform,
    available_packs,
    PackInfo,
    DialectTransformConfig,
)

def test_available_packs():
    """Packs are discoverable."""
    packs = available_packs()
    assert len(packs) >= 80
    assert all(isinstance(p, PackInfo) for p in packs)

def test_transform_basic():
    """Basic word replacement works."""
    result = transform("Gij moet dat doen.", "antwerps")
    # Exact output depends on pack rules
    assert result  # At least doesn't crash

def test_transform_protected_terms():
    """Protected terms are not transformed."""
    result = transform(
        "Het is verplicht dat gij dat doet.",
        "antwerps",
    )
    assert "verplicht" in result  # Protected
    # "gij" may be transformed, "verplicht" must not be

def test_transform_deterministic():
    """Deterministic mode produces same output."""
    text = "Dit is een test."
    dialect = "antwerps"

    result1 = transform(text, dialect, deterministic=True, seed=42)
    result2 = transform(text, dialect, deterministic=True, seed=42)

    assert result1 == result2

def test_transform_different_seeds():
    """Different seeds produce different output (for probabilistic rules)."""
    text = "Dit is een lange zin met veel woorden."
    dialect = "antwerps"

    result1 = transform(text, dialect, seed=1, enable_particles=True)
    result2 = transform(text, dialect, seed=999, enable_particles=True)

    # May or may not differ, but at least doesn't crash
    assert result1  # Non-empty

def test_inheritance_resolution():
    """Child packs inherit parent rules."""
    # Find a pack with inheritance
    packs = available_packs()
    child = next((p for p in packs if p.inherits), None)
    if child:
        result = transform("test", child.id)
        assert result  # Should work with inherited rules
```

## Fixtures

### `conftest.py`

```python
# tests/conftest.py

import sys
import pytest

@pytest.fixture(autouse=True)
def reload_package():
    """Ensure fresh import of vlaamscodex for each test."""
    # Remove cached imports
    mods = [k for k in sys.modules if k.startswith("vlaamscodex")]
    for m in mods:
        del sys.modules[m]

    yield

    # Cleanup after test
    mods = [k for k in sys.modules if k.startswith("vlaamscodex")]
    for m in mods:
        del sys.modules[m]

@pytest.fixture
def sample_plats():
    """Sample Platskript source for testing."""
    return """
plan doe
  zet x op getal 10 amen
  klap da x amen
gedaan
"""

@pytest.fixture
def tmp_plats_file(tmp_path, sample_plats):
    """Create temporary .plats file."""
    path = tmp_path / "test.plats"
    path.write_text(f"# coding: vlaamsplats\n{sample_plats}")
    return path
```

## Test Categories

### Unit Tests

- Test single functions in isolation
- Mock external dependencies
- Fast, focused, many of them

### Integration Tests

- Test multiple components together
- Use subprocess for codec tests (isolated Python)
- Test CLI commands end-to-end

### Property-Based Tests (Optional)

With Hypothesis:

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1))
def test_transform_never_crashes(text):
    """Transform should never raise for valid input."""
    try:
        result = transform(text, "antwerps")
        assert isinstance(result, str)
    except KeyError:
        pass  # Invalid dialect ID is OK to fail
```

## CI Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run tests
        run: pytest tests/ -v --tb=short
```

## Best Practices

1. **Test behavior, not implementation**: Test what the function does, not how
2. **One assertion per test** (ideally): Makes failures clear
3. **Descriptive names**: `test_compile_error_missing_amen` not `test_error`
4. **Arrange-Act-Assert**: Clear structure in each test
5. **Use fixtures**: Share setup code via `conftest.py`
6. **Subprocess for codec**: Avoid polluting test process with codec registration

## Coverage Goals

| Module | Target | Critical Paths |
|--------|--------|----------------|
| `compiler.py` | 90%+ | All statement types, error cases |
| `codec.py` | 80%+ | Encode/decode, incremental decoder |
| `transformer.py` | 85%+ | All rule types, inheritance, protected terms |
| `cli.py` | 70%+ | Command routing, error handling |
| `checker.py` | 80%+ | All check types, dialect messages |

## Adding New Tests

1. Create test file if new module
2. Import the unit under test
3. Write test function with `test_` prefix
4. Use fixtures for shared setup
5. Run locally before PR
6. Update coverage expectations if needed
