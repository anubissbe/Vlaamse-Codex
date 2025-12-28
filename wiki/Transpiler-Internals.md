# Transpiler Internals

> How Platskript becomes Python 🔧

This page documents the internal workings of the Platskript transpiler for developers who want to understand or extend it.

---

## Overview

The transpiler converts Platskript (`.plats`) source code into executable Python. It consists of two main components:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Platskript Transpiler                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────┐                                                      │
│  │   .plats file  │                                                      │
│  │ (Platskript)   │                                                      │
│  └───────┬────────┘                                                      │
│          │                                                               │
│          ├─────────────────┬─────────────────┐                          │
│          │                 │                 │                          │
│          ▼                 ▼                 ▼                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                │
│  │  plats run    │  │ python *.plats│  │ plats build   │                │
│  │  (explicit)   │  │ (magic mode)  │  │ (to .py file) │                │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘                │
│          │                  │                  │                        │
│          │           ┌──────┴──────┐           │                        │
│          │           │  codec.py   │           │                        │
│          │           │  (decode)   │           │                        │
│          │           └──────┬──────┘           │                        │
│          │                  │                  │                        │
│          ▼                  ▼                  ▼                        │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │                    compiler.py                               │        │
│  │                  compile_plats()                             │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                              │                                          │
│                              ▼                                          │
│                      ┌───────────────┐                                  │
│                      │ Python source │                                  │
│                      └───────────────┘                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Compiler (`compiler.py`)

### Entry Point

```python
from vlaamscodex.compiler import compile_plats

python_code = compile_plats(plats_source)
```

The `compile_plats()` function is the main entry point. It takes a Platskript source string and returns equivalent Python source code.

### Token-Based Approach

The compiler uses simple token parsing rather than a full AST. This is intentional for a parody language—keeps complexity low while being sufficient for the feature set.

```python
# Pseudocode of the compilation approach
def compile_plats(src):
    lines = []
    for line in src.split('\n'):
        tokens = tokenize(line)
        python_line = translate_tokens(tokens)
        lines.append(python_line)
    return '\n'.join(lines)
```

### Why Not an AST?

| Approach | Pros | Cons |
|----------|------|------|
| **Token-based** | Simple, ~200 lines | Limited grammar |
| **AST (Lark/ANTLR)** | Full grammar | Overkill for parody |

For Platskript's simple statement-oriented grammar, token parsing is sufficient.

---

## Operator Mapping (`OP_MAP`)

The `OP_MAP` dictionary translates Platskript operators to Python:

| Platskript | Python | Description |
|------------|--------|-------------|
| `plakt` | `+` | String concatenation |
| `derbij` | `+` | Addition |
| `deraf` | `-` | Subtraction |
| `keer` | `*` | Multiplication |
| `gedeeld` | `/` | Division |
| `isgelijk` | `==` | Equality |
| `isniegelijk` | `!=` | Inequality |
| `isgroterdan` | `>` | Greater than |
| `iskleinerdan` | `<` | Less than |

### Extending Operators

To add a new operator:

1. Add to `OP_MAP` in `compiler.py`:

```python
OP_MAP = {
    # ... existing operators
    'modulo': '%',      # New operator
}
```

2. Update `docs/04_language_spec.md`

3. Add tests in `tests/test_compiler.py`

---

## Statement Translation

### Statement Patterns

| Platskript Pattern | Python Output |
|--------------------|---------------|
| `plan doe ... gedaan` | (program wrapper) |
| `zet X op Y amen` | `X = Y` |
| `klap X amen` | `print(X)` |
| `maak funksie F met P doe ... gedaan` | `def F(P): ...` |
| `roep F met X amen` | `F(X)` |
| `geeftterug X amen` | `return X` |
| `als C dan doe ... gedaan` | `if C: ...` |
| `zolang C doe ... gedaan` | `while C: ...` |

### Translation Logic

```python
def translate_statement(tokens):
    if tokens[0] == 'zet':
        # zet X op Y amen → X = Y
        var_name = tokens[1]
        value = translate_expression(tokens[3:-1])  # Skip 'op' and 'amen'
        return f"{var_name} = {value}"

    elif tokens[0] == 'klap':
        # klap X amen → print(X)
        expr = translate_expression(tokens[1:-1])
        return f"print({expr})"

    elif tokens[0] == 'maak' and tokens[1] == 'funksie':
        # maak funksie F met P doe → def F(P):
        name = tokens[2]
        params = extract_params(tokens)
        return f"def {name}({params}):"

    # ... etc
```

---

## Expression Translation

### Expression Types

| Platskript | Python |
|------------|--------|
| `tekst hello world` | `'hello world'` |
| `getal 42` | `42` |
| `da variabele` | `variabele` |
| `spatie` | `' '` |
| `X plakt Y` | `X + Y` |
| `X derbij Y` | `X + Y` |

### The `da` Reference

Variables must be referenced with `da` to distinguish them from literal text:

```platskript
zet naam op tekst Claude amen    # naam = 'Claude'
klap da naam amen                # print(naam)
```

Without `da`:
```platskript
klap naam amen                   # Would print literal 'naam'
```

---

## Block Handling

### Block Structure

```platskript
plan doe                         # Opens program block
  zet x op getal 5 amen
  klap da x amen
gedaan                           # Closes program block
```

### Indentation Management

The compiler tracks indentation levels:

```python
indent_level = 0
output = []

for line in source_lines:
    if 'doe' in line:
        output.append(' ' * indent_level * 4 + translate(line))
        indent_level += 1
    elif line.strip() == 'gedaan':
        indent_level -= 1
    else:
        output.append(' ' * indent_level * 4 + translate(line))
```

---

## Function Handling

### Definition

```platskript
maak funksie greet met wie doe
  klap tekst hello plakt spatie plakt da wie amen
gedaan
```

Becomes:

```python
def greet(wie):
    print('hello' + ' ' + wie)
```

### Calling

```platskript
roep greet met tekst world amen
```

Becomes:

```python
greet('world')
```

### Return Values

```platskript
maak funksie dubbel met n doe
  geeftterug da n keer getal 2 amen
gedaan
```

Becomes:

```python
def dubbel(n):
    return n * 2
```

---

## Error Handling

### Syntax Errors

The compiler raises `SyntaxError` for:

| Error | Example |
|-------|---------|
| Missing `amen` | `klap tekst hello` |
| Missing `gedaan` | Unclosed block |
| Unknown keyword | `print tekst hello amen` |

### Error Messages

```python
def raise_error(line_num, message):
    raise SyntaxError(f"Line {line_num}: {message}")
```

---

## Codec (`codec.py`)

The codec enables "magic mode" where Python can directly execute `.plats` files.

### How It Works

1. **Registration**: At Python startup, codec registers via `.pth` hook
2. **Detection**: Python sees `# coding: vlaamsplats` in source file
3. **Decoding**: Python calls our codec to "decode" the file
4. **Transformation**: Codec calls `compile_plats()` and returns Python source
5. **Execution**: Python parses and executes the returned Python code

### Codec Structure

```python
class VlaamsPlatsCodec(codecs.Codec):
    def decode(self, input_bytes, errors='strict'):
        # 1. Decode bytes as UTF-8 to get Plats source
        plats_src = input_bytes.decode('utf-8')

        # 2. Compile to Python
        python_src = compile_plats(plats_src)

        # 3. Return Python source (as if we "decoded" it)
        return python_src, len(input_bytes)
```

### Registration

```python
def search_function(encoding_name):
    if encoding_name == 'vlaamsplats':
        return codecs.CodecInfo(
            name='vlaamsplats',
            encode=...,
            decode=VlaamsPlatsCodec().decode,
            ...
        )
    return None

codecs.register(search_function)
```

**See:** [[Magic-Mode]] for complete codec documentation.

---

## Limitations

### Grammar Limitations

The token-based approach limits grammar complexity:

| Limitation | Example |
|------------|---------|
| No nested expressions | `(a plakt b) keer c` not supported |
| String literals consume to end | Can't have operators after text |
| No multi-line statements | Each statement on one line |

### Error Reporting

Since the transpiler operates before Python's parser:
- Line numbers in tracebacks refer to generated Python
- Error messages are Python errors, not Platskript-native

**Future improvement**: Implement source maps for Plats → Python line mapping.

---

## Files

| File | Purpose |
|------|---------|
| `src/vlaamscodex/compiler.py` | Main transpiler logic |
| `src/vlaamscodex/codec.py` | Python source encoding codec |
| `data/vlaamscodex_autoload.pth` | Startup hook for codec registration |
| `vlaamscodex_build_backend.py` | Custom build backend for .pth injection |

---

## Extending the Compiler

### Adding New Statements

1. Add pattern recognition in the token translator:

```python
def translate_tokens(tokens):
    if tokens[0] == 'nieuw_keyword':
        # Handle new statement type
        return translate_new_statement(tokens)
    # ... existing patterns
```

2. Generate appropriate Python output

3. Document in language spec

4. Add tests

### Example: Adding a Loop Statement

```python
# In compiler.py
def translate_tokens(tokens):
    # ... existing code ...

    if tokens[0] == 'herhaal':
        # herhaal N keer doe ... gedaan
        count = translate_expression([tokens[1]])
        return f"for _i in range({count}):"
```

---

## Testing the Transpiler

### Unit Tests

```python
def test_compile_simple_print():
    plats = "klap tekst hello amen"
    result = compile_plats(plats)
    assert "print" in result
    assert "'hello'" in result

def test_compile_variable_assignment():
    plats = "zet x op getal 42 amen"
    result = compile_plats(plats)
    assert "x = 42" in result
```

### Integration Tests

```python
def test_run_complete_program():
    plats = """
# coding: vlaamsplats
plan doe
  zet x op getal 5 amen
  klap da x amen
gedaan
"""
    result = run_plats(plats)
    assert "5" in result.stdout
```

---

## See Also

- [[Magic-Mode]] - Codec system details
- [[Language-Reference]] - Platskript syntax
- [[Architecture-Overview]] - System design
- [[Contributing]] - How to contribute

---

**Veel plansen!** 🧇
