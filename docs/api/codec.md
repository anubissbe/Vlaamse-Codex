# codec.py - Python Source Encoding

> `src/vlaamscodex/codec.py`

Custom Python source encoding that enables "magic mode" - running `.plats` files directly with `python script.plats`.

## Overview

This module registers a custom codec (`vlaamsplats`) with Python's codec system. When Python encounters `# coding: vlaamsplats` at the top of a file, it uses this codec to decode the source, which intercepts the raw bytes and returns transpiled Python instead.

## Functions

### `register() -> None`

Register the `vlaamsplats` codec search function with Python.

**Usage:**
```python
from vlaamscodex.codec import register
register()  # Now Python recognizes 'coding: vlaamsplats'
```

This is typically called automatically via the `.pth` startup hook installed to `site-packages`.

---

## How Magic Mode Works

### 1. Startup Hook

When the package is installed, `data/vlaamscodex_autoload.pth` is placed in `site-packages`. This file runs:

```python
import vlaamscodex.codec; vlaamscodex.codec.register()
```

### 2. Codec Registration

`register()` adds a search function to `codecs.register()` that matches:
- `vlaamsplats`
- `plats`

### 3. File Execution

When you run `python script.plats`:

1. Python reads `# coding: vlaamsplats` from line 1
2. Python looks up the `vlaamsplats` codec
3. Our codec's `decode()` receives the raw bytes
4. We transpile Platskript → Python
5. Python receives valid Python source
6. Python executes the result

---

## Internal Classes

### `Codec`

Standard codec implementing `encode()` and `decode()`.

- **encode**: Passes through to UTF-8 (write operations)
- **decode**: Transpiles Platskript to Python

### `IncrementalDecoder`

Buffers input until `final=True`, then transpiles all at once.

### `StreamReader`

Wraps file streams, compiling on first read.

### `StreamWriter`

Passes through to UTF-8 for write operations.

---

## Example

```python
# myscript.plats
# coding: vlaamsplats
plan doe
  klap tekst gdag weeireld amen
gedaan
```

```bash
# After package installation, this just works:
python myscript.plats
# Output: gdag weeireld
```

---

## Build System Integration

The custom build backend (`vlaamscodex_build_backend.py`) ensures the `.pth` file is included in wheels, enabling automatic codec registration on package installation.

See: [Architecture: Transpiler](../architecture/01_transpiler.md)
