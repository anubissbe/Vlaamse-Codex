# compiler.py - Platskript Transpiler

> `src/vlaamscodex/compiler.py`

Token-based transpiler that converts Platskript source code to Python.

## Overview

The compiler uses simple line-by-line token parsing to transform Platskript syntax into equivalent Python code. It's intentionally simple ("toy compiler") for readability.

## Functions

### `compile_plats(plats_src: str) -> str`

Main entry point. Compiles Platskript source to Python source.

**Parameters:**
- `plats_src` (str): Platskript source code

**Returns:**
- `str`: Generated Python source code

**Raises:**
- `ValueError`: On syntax errors (missing 'amen', unclosed blocks, etc.)

**Example:**
```python
from vlaamscodex.compiler import compile_plats

plats_code = """
plan doe
  klap tekst hallo amen
gedaan
"""

python_code = compile_plats(plats_code)
# Output: print('hallo')
```

---

### `_parse_expr(tokens: list[str]) -> str`

Parse a Platskript expression into a Python expression string.

**Internal function** - handles expression parsing for:
- `tekst <words>` → string literals
- `getal <n>` → number literals
- `da <name>` → variable references
- `spatie` → space character
- Operators (see `OP_MAP`)

---

### `_split_args(tokens: list[str]) -> list[list[str]]`

Split argument tokens separated by `en` keyword.

**Internal function** - used for parsing function call arguments.

---

## Constants

### `OP_MAP`

Dictionary mapping Platskript operators to Python equivalents.

```python
OP_MAP = {
    "plakt": "+",        # String concatenation
    "derbij": "+",       # Addition
    "deraf": "-",        # Subtraction
    "keer": "*",         # Multiplication
    "gedeeld": "/",      # Division
    "isgelijk": "==",    # Equality
    "isniegelijk": "!=", # Inequality
    "isgroterdan": ">",  # Greater than
    "iskleinerdan": "<", # Less than
    "enook": "and",      # Logical AND
    "ofwel": "or",       # Logical OR
    "nie": "not",        # Logical NOT
}
```

**Extending:** Add new operators here and update `docs/04_language_spec.md`.

---

## Supported Constructs

| Platskript | Python | Notes |
|------------|--------|-------|
| `plan doe ... gedaan` | (program wrapper) | Entry point |
| `zet X op Y amen` | `X = Y` | Assignment |
| `klap X amen` | `print(X)` | Print |
| `maak funksie X met ... doe` | `def X(...):` | Function definition |
| `roep X met Y amen` | `X(Y)` | Function call |
| `geeftterug X amen` | `return X` | Return statement |

---

## Error Handling

The compiler raises `ValueError` for:

1. **Missing `amen`**: Statement terminator required
2. **Missing `gedaan`**: Block must be closed
3. **Unclosed blocks**: `plan doe` without matching `gedaan`
4. **Invalid numbers**: `getal` without valid numeric literal
5. **Unknown instructions**: Unrecognized statement patterns
