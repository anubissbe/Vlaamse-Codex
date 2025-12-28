# VlaamsCodex API Reference

> **Version**: 0.2.0 | **Python**: >=3.10

This directory contains API documentation for the VlaamsCodex Python package.

## Module Index

| Module | Purpose | Key Exports |
|--------|---------|-------------|
| [compiler](compiler.md) | Platskript → Python transpiler | `compile_plats()`, `OP_MAP` |
| [codec](codec.md) | Python source encoding for magic mode | `register()` |
| [transformer](transformer.md) | Dialect text transformation engine | `transform()`, `available_packs()` |
| [cli](cli.md) | Multi-dialect CLI entry point | `main()`, `COMMAND_ALIASES` |
| [checker](checker.md) | Syntax validation | `check_syntax()`, `check_file()` |
| [repl](repl.md) | Interactive REPL | `run_repl()` |
| [examples](examples.md) | Example browser | `run_example()`, `list_examples()` |
| [fortune](fortune.md) | Proverb easter egg | `get_fortune()`, `print_fortune()` |
| [init](init.md) | Project scaffolding | `create_project()` |

## Quick Links

- [Getting Started](../06_user_guide.md)
- [Language Specification](../04_language_spec.md)
- [Architecture Overview](../architecture/00_overview.md)

## Import Patterns

```python
# Transpiler
from vlaamscodex.compiler import compile_plats

# Dialect transformation
from vlaamscodex.dialects.transformer import transform, available_packs

# Syntax checking
from vlaamscodex.checker import check_syntax, check_file
```
