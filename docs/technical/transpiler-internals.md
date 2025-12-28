# Transpiler Internals

> Deep dive into the Platskript → Python compilation process.

## Design Philosophy

The VlaamsCodex transpiler is intentionally **simple** ("toy compiler"):

- **Line-by-line processing**: No AST, no parser generator
- **Token splitting**: Simple `str.split()` on whitespace
- **Pattern matching**: Sequential if/elif checks
- **Readable over optimal**: Educational clarity over performance

This makes it easy to understand and extend, suitable for a parody language.

## Compilation Pipeline

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Platskript     │────▶│  compile_plats() │────▶│  Python Source  │
│  Source Code    │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
         ┌──────────────┐          ┌──────────────┐
         │ Line-by-line │          │  Expression  │
         │   Tokenize   │          │   Parsing    │
         └──────────────┘          └──────────────┘
```

## Core Functions

### `compile_plats(plats_src: str) -> str`

Main entry point. Processes source line-by-line:

```python
def compile_plats(plats_src: str) -> str:
    py_lines: list[str] = []
    indent = 0
    stack: list[str] = []  # Track block types

    def emit(line: str) -> None:
        py_lines.append(("    " * indent) + line)

    for raw in plats_src.splitlines():
        line = raw.strip()
        if not line:
            continue

        tokens = line.split()
        # ... pattern matching logic ...

    return "\n".join(py_lines) + "\n"
```

### Block Tracking

The `stack` tracks open blocks for proper nesting:

```python
# Opening blocks
if tokens[:2] == ["plan", "doe"]:
    stack.append("plan")
    continue

if tokens[:2] == ["maak", "funksie"]:
    stack.append("funksie")
    indent += 1
    # ... emit def statement ...

# Closing blocks
if tokens == ["gedaan"]:
    kind = stack.pop()
    if kind == "funksie":
        indent -= 1
    continue
```

### Statement Pattern Matching

Each statement type is matched by its opening tokens:

```python
# Statement must end with 'amen'
if tokens[-1] != "amen":
    raise ValueError(f"missing 'amen': {line}")
tokens = tokens[:-1]  # Strip terminator

# Print statement
if tokens[0] == "klap":
    emit(f"print({_parse_expr(tokens[1:])})")
    continue

# Assignment
if tokens[0] == "zet":
    # zet X op Y amen
    op_i = tokens.index("op")
    var = tokens[1]
    emit(f"{var} = {_parse_expr(tokens[op_i + 1:])}")
    continue

# Function call
if tokens[0] == "roep":
    # roep X met Y amen
    func = tokens[1]
    if "met" in tokens:
        met_i = tokens.index("met")
        args = [_parse_expr(a) for a in _split_args(tokens[met_i + 1:])]
        emit(f"{func}({', '.join(args)})")
    else:
        emit(f"{func}()")
    continue
```

## Expression Parsing

### `_parse_expr(tokens: list[str]) -> str`

Converts Platskript expressions to Python:

```python
def _parse_expr(tokens: list[str]) -> str:
    parts: list[str] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]

        # Stop words (block keywords)
        if t in {"dan", "doe", "amen"}:
            break

        # Space literal
        if t == "spatie":
            parts.append(repr(" "))
            i += 1
            continue

        # String literal: tekst word1 word2 ...
        if t == "tekst":
            i += 1
            words = []
            while i < len(tokens) and tokens[i] not in OP_MAP and tokens[i] not in {"dan", "doe", "amen", "en"}:
                words.append(tokens[i])
                i += 1
            parts.append(repr(" ".join(words)))
            continue

        # Number literal: getal 123
        if t == "getal":
            i += 1
            num = tokens[i]
            i += 1
            parts.append(num)
            continue

        # Variable reference: da X
        if t == "da":
            i += 1
            parts.append(tokens[i])
            i += 1
            continue

        # Operator
        if t in OP_MAP:
            parts.append(OP_MAP[t])
            i += 1
            continue

        # Fallback: bare identifier
        parts.append(t)
        i += 1

    return " ".join(parts) if parts else "None"
```

### Operator Map

```python
OP_MAP = {
    # String operations
    "plakt": "+",         # Concatenation

    # Arithmetic
    "derbij": "+",        # Addition
    "deraf": "-",         # Subtraction
    "keer": "*",          # Multiplication
    "gedeeld": "/",       # Division

    # Comparison
    "isgelijk": "==",     # Equality
    "isniegelijk": "!=",  # Inequality
    "isgroterdan": ">",   # Greater than
    "iskleinerdan": "<",  # Less than

    # Boolean
    "enook": "and",       # Logical AND
    "ofwel": "or",        # Logical OR
    "nie": "not",         # Logical NOT
}
```

## Compilation Examples

### Hello World

```platskript
plan doe
  klap tekst gdag weeireld amen
gedaan
```

Compiles to:

```python
print('gdag weeireld')
```

### Function Definition

```platskript
plan doe
  maak funksie groet met naam doe
    klap tekst hallo plakt spatie plakt da naam amen
  gedaan
  roep groet met tekst wereld amen
gedaan
```

Compiles to:

```python
def groet(naam):
    print('hallo' + ' ' + naam)
groet('wereld')
```

### Arithmetic

```platskript
plan doe
  zet x op getal 10 amen
  zet y op da x derbij getal 5 amen
  klap da y amen
gedaan
```

Compiles to:

```python
x = 10
y = x + 5
print(y)
```

## Error Handling

### Syntax Errors

```python
# Missing terminator
if tokens[-1] != "amen":
    raise ValueError(f"missing 'amen' statement terminator: {line}")

# Unclosed blocks
if stack:
    raise ValueError(f"unclosed blocks: {stack}")

# Unknown instruction
raise ValueError(f"unknown instruction: {line}")
```

### Expression Errors

```python
# Missing number after 'getal'
if t == "getal" and i >= len(tokens):
    raise ValueError("getal without value")

# Missing identifier after 'da'
if t == "da" and i >= len(tokens):
    raise ValueError("da without identifier")
```

## Extending the Transpiler

### Adding New Operators

1. Add to `OP_MAP`:
   ```python
   OP_MAP["modulo"] = "%"
   ```

2. Update `docs/04_language_spec.md`

### Adding New Statement Types

1. Add pattern match in `compile_plats()`:
   ```python
   if tokens[0] == "nieuwinstructie":
       # Parse and emit
       emit(...)
       continue
   ```

2. Add tests in `tests/test_compiler.py`

### Adding Control Flow

Current implementation doesn't have if/while. To add:

```python
# If statement: als CONDITION dan doe ... gedaan
if tokens[0] == "als" and "dan" in tokens and "doe" in tokens:
    dan_i = tokens.index("dan")
    condition = _parse_expr(tokens[1:dan_i])
    emit(f"if {condition}:")
    indent += 1
    stack.append("als")
    continue
```

## Limitations

1. **No AST**: Can't do complex transformations or optimizations
2. **Whitespace tokenization**: Can't have operators within identifiers
3. **No error recovery**: First error stops compilation
4. **No source maps**: Can't trace Python errors back to Platskript lines
5. **Single-pass**: Can't do forward references

These are intentional for simplicity. A production language would use a proper parser.
