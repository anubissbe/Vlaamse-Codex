# API Reference

> Python module documentation 📚

This page documents the public Python API for VlaamsCodex.

---

## Installation

```bash
pip install vlaamscodex
```

---

## Quick Import

```python
# Transpiler
from vlaamscodex.compiler import compile_plats

# Dialect transformer
from vlaamscodex.dialects.transformer import transform, available_packs

# Version
import vlaamscodex
print(vlaamscodex.__version__)
```

---

## Compiler Module

> `src/vlaamscodex/compiler.py`

### `compile_plats(source: str) -> str`

Compile Platskript source code to Python.

**Parameters:**
- `source` (str): Platskript source code

**Returns:**
- `str`: Equivalent Python source code

**Raises:**
- `SyntaxError`: If the Platskript code is invalid

**Example:**

```python
from vlaamscodex.compiler import compile_plats

plats = """
plan doe
  zet naam op tekst Claude amen
  klap da naam amen
gedaan
"""

python_code = compile_plats(plats)
print(python_code)
# Output:
# naam = 'Claude'
# print(naam)
```

---

## Codec Module

> `src/vlaamscodex/codec.py`

### `register()`

Register the `vlaamsplats` codec with Python's codec registry.

**Note:** This is called automatically at Python startup via the `.pth` hook. You typically don't need to call this manually.

**Example:**

```python
from vlaamscodex.codec import register

# Force registration (rarely needed)
register()

# Verify
import codecs
print(codecs.lookup('vlaamsplats'))
```

---

## Dialect Transformer Module

> `src/vlaamscodex/dialects/transformer.py`

### `transform(text: str, dialect_id: str, **kwargs) -> str`

Transform text using a dialect pack.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | str | (required) | Input text to transform |
| `dialect_id` | str | (required) | Dialect pack ID (e.g., `"antwerps"`) |
| `deterministic` | bool | `True` | Use deterministic randomness |
| `seed` | int | `0` | Seed for deterministic mode |
| `enable_particles` | bool | `False` | Add dialect particles |
| `pronoun_subject` | str | `"ge"` | Subject pronoun |
| `pronoun_object` | str | `"u"` | Object pronoun |
| `pronoun_possessive` | str | `"uw"` | Possessive pronoun |
| `max_passes` | int | `3` | Maximum transformation passes |
| `strict_idempotency` | bool | `False` | Raise on non-convergence |

**Returns:**
- `str`: Transformed text

**Example:**

```python
from vlaamscodex.dialects.transformer import transform

# Basic transformation
text = "Gij hebt dat goed gedaan"
result = transform(text, "antwerps")
print(result)  # "Ge hebt da goe gedaan"

# With particles
result = transform(text, "antwerps", enable_particles=True)
print(result)  # "Ge hebt da goe gedaan, zansen"

# Deterministic with custom seed
result = transform(text, "antwerps", deterministic=True, seed=42)
```

---

### `available_packs() -> list[PackInfo]`

List all available dialect packs.

**Returns:**
- `list[PackInfo]`: Sorted list of pack metadata

**Example:**

```python
from vlaamscodex.dialects.transformer import available_packs

for pack in available_packs():
    print(f"{pack.id}: {pack.label}")
    if pack.inherits:
        print(f"  inherits: {', '.join(pack.inherits)}")
```

**Output:**

```
algemeen-vlaams: Algemeen Vlaams
antwerps: Antwerps
  inherits: algemeen-vlaams
brussels: Brussels
  inherits: algemeen-vlaams
...
```

---

### `PackInfo`

Metadata about a dialect pack.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PackInfo:
    id: str           # e.g., "antwerps"
    label: str        # e.g., "Antwerps"
    inherits: tuple[str, ...]  # Parent pack IDs
```

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Pack identifier |
| `label` | str | Human-readable name |
| `inherits` | tuple[str, ...] | Parent pack IDs |

---

### `DialectTransformConfig`

Configuration dataclass for transformation behavior.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DialectTransformConfig:
    deterministic: bool = True
    seed: int = 0
    enable_particles: bool = False
    pronoun_subject: str = "ge"
    pronoun_object: str = "u"
    pronoun_possessive: str = "uw"
    max_passes: int = 3
    strict_idempotency: bool = False
```

**Usage:**

```python
from vlaamscodex.dialects.transformer import transform, DialectTransformConfig

config = DialectTransformConfig(
    deterministic=True,
    seed=42,
    enable_particles=True,
    max_passes=5
)

# Note: Currently config is passed via kwargs, not as object
result = transform(text, "antwerps", **config.__dict__)
```

---

## REPL Module

> `src/vlaamscodex/repl.py`

### `run_repl(dialect: str = None)`

Start the interactive Platskript REPL.

**Parameters:**
- `dialect` (str, optional): Dialect for error messages

**Example:**

```python
from vlaamscodex.repl import run_repl

# Start REPL (blocking)
run_repl()

# With dialect-specific errors
run_repl(dialect="antwerps")
```

---

## Checker Module

> `src/vlaamscodex/checker.py`

### `check_file(path: str, dialect: str = None) -> bool`

Check a Platskript file for syntax errors.

**Parameters:**
- `path` (str): Path to `.plats` file
- `dialect` (str, optional): Dialect for error messages

**Returns:**
- `bool`: `True` if valid, `False` if errors found

**Example:**

```python
from vlaamscodex.checker import check_file

if check_file("script.plats"):
    print("File is valid!")
else:
    print("Syntax errors found")
```

---

## Examples Module

> `src/vlaamscodex/examples.py`

### `list_examples() -> list[str]`

List available example names.

**Returns:**
- `list[str]`: Names of available examples

### `get_example(name: str) -> str`

Get example source code.

**Parameters:**
- `name` (str): Example name

**Returns:**
- `str`: Example source code

**Example:**

```python
from vlaamscodex.examples import list_examples, get_example

# List examples
for name in list_examples():
    print(name)

# Get example source
source = get_example("hello")
print(source)
```

---

## Fortune Module

> `src/vlaamscodex/fortune.py`

### `get_fortune() -> str`

Get a random Flemish proverb.

**Returns:**
- `str`: A proverb or wisdom

**Example:**

```python
from vlaamscodex.fortune import get_fortune

print(get_fortune())
# "Beter een vogel in de hand dan tien op 't dak, jong!"
```

---

## Init Module

> `src/vlaamscodex/init.py`

### `init_project(name: str, path: str = ".")`

Create a new Platskript project.

**Parameters:**
- `name` (str): Project name
- `path` (str): Base path (default: current directory)

**Creates:**
```
{name}/
├── hallo.plats      # Sample program
└── LEESMIJ.md       # Quick start guide
```

**Example:**

```python
from vlaamscodex.init import init_project

init_project("mijnproject")
# Creates mijnproject/ directory with starter files
```

---

## Environment Variables

These environment variables affect module behavior:

### Compiler/Codec

| Variable | Default | Description |
|----------|---------|-------------|
| (none) | - | Compiler has no env var configuration |

### Dialect Transformer

| Variable | Default | Description |
|----------|---------|-------------|
| `VLAAMSCODEX_DIALECTS_DIR` | auto | Path to dialects directory |
| `VLAAMSCODEX_DIALECT_DETERMINISTIC` | `True` | Deterministic mode |
| `VLAAMSCODEX_DIALECT_SEED` | `0` | Random seed |
| `VLAAMSCODEX_DIALECT_PARTICLES` | `False` | Enable particles |
| `VLAAMSCODEX_PRONOUN_SUBJECT` | `ge` | Subject pronoun |
| `VLAAMSCODEX_PRONOUN_OBJECT` | `u` | Object pronoun |
| `VLAAMSCODEX_PRONOUN_POSSESSIVE` | `uw` | Possessive pronoun |
| `VLAAMSCODEX_DIALECT_MAX_PASSES` | `3` | Max transformation passes |
| `VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY` | `False` | Raise on non-convergence |

---

## Version

```python
import vlaamscodex
print(vlaamscodex.__version__)  # "0.2.0"
```

---

## Type Hints

VlaamsCodex uses type hints for public APIs. For development:

```python
from vlaamscodex.dialects.transformer import transform, PackInfo

# Type-safe usage
def process_text(text: str) -> str:
    return transform(text, "antwerps")

def list_dialects() -> list[PackInfo]:
    from vlaamscodex.dialects.transformer import available_packs
    return available_packs()
```

---

## Complete Example

```python
#!/usr/bin/env python3
"""Complete VlaamsCodex API usage example."""

from vlaamscodex.compiler import compile_plats
from vlaamscodex.dialects.transformer import transform, available_packs

# 1. Compile Platskript to Python
plats_code = """
plan doe
  zet naam op tekst weeireld amen
  maak funksie groet met wie doe
    klap tekst gdag plakt spatie plakt da wie amen
  gedaan
  roep groet met da naam amen
gedaan
"""

python_code = compile_plats(plats_code)
print("=== Generated Python ===")
print(python_code)
print()

# 2. Transform text to dialects
text = "Gij hebt dat goed gedaan vandaag"

print("=== Dialect Transformations ===")
for pack in available_packs()[:5]:  # First 5
    result = transform(text, pack.id)
    print(f"{pack.label:20} → {result}")
print()

# 3. With particles
print("=== With Particles ===")
result = transform(text, "antwerps", enable_particles=True)
print(f"Antwerps: {result}")
```

---

## See Also

- [[Transpiler-Internals]] - How compilation works
- [[Dialect-Engine]] - Transformation internals
- [[Architecture-Overview]] - System design
- [[CLI-Reference]] - Command-line interface

---

**Veel plansen!** 🧇
