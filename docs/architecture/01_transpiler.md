# Platskript Transpiler Architecture

The transpiler converts Platskript (`.plats`) source code into executable Python. It consists of two main components: the compiler and the codec.

## Overview

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

## Compiler (`compiler.py`)

### Entry Point

```python
from vlaamscodex.compiler import compile_plats

python_code = compile_plats(plats_source)
```

### Token-Based Approach

The compiler uses simple token parsing rather than a full AST. This is appropriate for Platskript's limited grammar:

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

### Operator Mapping (`OP_MAP`)

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

### Statement Translation

| Platskript Pattern | Python Output |
|--------------------|---------------|
| `plan doe ... gedaan` | (program wrapper, no direct output) |
| `zet X op Y amen` | `X = Y` |
| `klap X amen` | `print(X)` |
| `maak funksie F met P doe ... gedaan` | `def F(P): ...` |
| `roep F met X amen` | `F(X)` |
| `geeftterug X amen` | `return X` |

### Expression Translation

| Platskript | Python |
|------------|--------|
| `tekst hello world` | `"hello world"` |
| `getal 42` | `42` |
| `da variabele` | `variabele` |
| `spatie` | `" "` |

## Codec (`codec.py`)

The codec enables "magic mode" where Python can directly execute `.plats` files.

### How It Works

1. **Registration**: At Python startup, the codec is registered via `.pth` hook
2. **Detection**: Python sees `# coding: vlaamsplats` in the source file
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

The codec is registered using Python's codec registry:

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

## Startup Hook

### The `.pth` File

`data/vlaamscodex_autoload.pth`:
```
import vlaamscodex.codec as _vc; _vc.register()
```

### Why `.pth`?

Python's `site` module processes `.pth` files at startup, BEFORE loading user scripts. This ensures the codec is available when Python tries to decode a `.plats` file.

### Build Backend

`vlaamscodex_build_backend.py` is a custom PEP 517 build backend that:

1. Wraps `setuptools.build_meta`
2. Injects `vlaamscodex_autoload.pth` into the wheel's `*.data/data/` directory
3. Ensures the `.pth` file lands in `site-packages` upon installation

## Limitations

### Magic Mode Restrictions

Magic mode (`python script.plats`) fails when:
- `python -S` (disables site initialization)
- `python -I` (isolated mode)
- Embedded Python without site processing

**Workaround**: Use `plats run script.plats` instead.

### Error Reporting

Since the transpiler operates before Python's parser:
- Line numbers in tracebacks refer to generated Python, not original Platskript
- Error messages are Python errors, not Platskript-native

Future improvement: implement source maps for Plats → Python line mapping.

### Grammar Limitations

The token-based approach limits grammar complexity:
- No nested expressions (e.g., `(a plakt b) keer c`)
- String literals consume to end of expression
- No multi-line statements

For a production language, a proper parser (Lark/ANTLR) would be needed.

## Files

| File | Purpose |
|------|---------|
| `src/vlaamscodex/compiler.py` | Main transpiler logic |
| `src/vlaamscodex/codec.py` | Python source encoding codec |
| `data/vlaamscodex_autoload.pth` | Startup hook for codec registration |
| `vlaamscodex_build_backend.py` | Custom build backend for .pth injection |

## Extending the Compiler

### Adding New Operators

1. Add to `OP_MAP` in `compiler.py`:
   ```python
   OP_MAP = {
       ...
       'nieuw_operator': 'python_op',
   }
   ```

2. Update `docs/04_language_spec.md`

### Adding New Statements

1. Add pattern recognition in the token translator
2. Generate appropriate Python output
3. Document in language spec
