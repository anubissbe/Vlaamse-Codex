# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VlaamsCodex is a transpiler toolchain for **Platskript** (`.plats`), a parody programming language using Flemish dialect keywords. The system compiles Platskript source code to Python and supports transparent execution via Python's source encoding mechanism (PEP 263).

## Development Commands

```bash
# Create virtual environment and install in development mode
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Execute a Platskript program
plats run examples/hello.plats

# Display generated Python source
plats show-python examples/hello.plats

# Compile to Python file
plats build examples/hello.plats --out output.py

# Magic mode execution (requires installation)
python examples/hello.plats

# Run test suite
pytest tests/

# Run specific test
pytest tests/test_compiler.py::test_compile_plats_hello_shape -v

# Build distribution packages
python -m build
```

## Architecture

### Core Modules (`src/vlaamscodex/`)

#### compiler.py
Platskript-to-Python transpiler implementing line-by-line parsing with stack-based block tracking.

- `compile_plats(plats_src: str) -> str` — Main compilation entry point
- `OP_MAP` — Operator mapping dictionary (Platskript → Python)
- `_parse_expr()` — Expression parser
- `_split_args()` — Argument list tokenizer

#### codec.py
Custom Python source encoding codec registered as `vlaamsplats`.

- `register()` — Registers codec with Python's codec registry (called at startup)
- `_compile_plats_bytes()` — Core transformation: UTF-8 decode → strip encoding header → transpile → return Python source
- Implements full codec protocol: `Codec`, `IncrementalDecoder`, `StreamReader`, `StreamWriter`

#### cli.py
Command-line interface providing the `plats` command.

- Subcommands: `run`, `build`, `show-python`
- `_read_plats()` — File reader that strips encoding declarations

### Magic Mode Execution Chain

1. **Startup Hook**: `data/vlaamscodex_autoload.pth` installed to site-packages root
2. **Hook Content**: `import vlaamscodex.codec as _vc; _vc.register()`
3. **Trigger**: Python encounters `# coding: vlaamsplats` (PEP 263)
4. **Transformation**: Codec transparently transpiles Platskript → Python before execution

### Build System

#### vlaamscodex_build_backend.py
Custom PEP 517 build backend wrapping setuptools to inject the `.pth` file into wheel distributions.

- `_ensure_autoload_pth_in_wheel()` — Post-processes wheel to include startup hook
- Updates RECORD manifest with correct file hash

## Language Syntax Reference

Programs are enclosed in `plan doe ... gedaan`. Statements terminate with `amen`.

### Statement Forms

| Statement | Syntax |
|-----------|--------|
| Assignment | `zet <var> op <expr> amen` |
| Print | `klap <expr> amen` |
| Function Definition | `maak funksie <name> met <params> doe ... gedaan` |
| Function Call | `roep <name> met <args> amen` |
| Return | `geeftterug <expr> amen` |

### Expression Forms

| Expression | Result |
|------------|--------|
| `tekst <words>` | String literal |
| `getal <n>` | Numeric literal |
| `da <var>` | Variable reference |
| `spatie` | Space character |
| `plakt` | Concatenation operator |

### Operator Mappings

Defined in `OP_MAP`: `plakt`→`+`, `derbij`→`+`, `deraf`→`-`, `keer`→`*`, `gedeeld`→`/`, `isgelijk`→`==`, `isniegelijk`→`!=`, `isgroterdan`→`>`, `iskleinerdan`→`<`, `enook`→`and`, `ofwel`→`or`, `nie`→`not`

## Known Limitations

- `python -S` disables site module — `.pth` hooks do not execute
- `python -I` (isolated mode) restricts site-packages access
- Fallback: `plats run script.plats` operates without startup hooks
- Compiler uses simplified line-by-line parsing (no formal AST)
