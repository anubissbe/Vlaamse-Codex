# Technical Documentation

> Deep-dive technical documentation for VlaamsCodex developers and contributors.

## Contents

| Document | Audience | Purpose |
|----------|----------|---------|
| [Build System](build-system.md) | Package maintainers | PEP 517 custom backend, wheel injection |
| [Transpiler Internals](transpiler-internals.md) | Language extenders | Token parsing, code generation |
| [Dialect Engine](dialect-engine.md) | Dialect creators | Rule processing, inheritance, protected terms |
| [Testing Strategy](testing.md) | Contributors | Test patterns, fixtures, coverage |
| [Contributing](contributing.md) | All contributors | Setup, workflow, code standards |

## Quick Reference

### Project Layout

```
Vlaamse-Codex/
├── src/vlaamscodex/           # Python package
│   ├── __init__.py            # Version, package metadata
│   ├── compiler.py            # Platskript → Python transpiler
│   ├── codec.py               # Magic mode encoding
│   ├── cli.py                 # Multi-dialect CLI router
│   ├── repl.py                # Interactive REPL
│   ├── checker.py             # Syntax validation
│   ├── examples.py            # Example browser
│   ├── fortune.py             # Proverb easter egg
│   ├── init.py                # Project scaffolding
│   └── dialects/              # Dialect subsystem
│       └── transformer.py     # Rule engine
│
├── dialects/                  # Dialect data (not Python)
│   ├── index.json             # Pack registry
│   └── packs/*.json           # 83 dialect packs
│
├── data/                      # Package data
│   └── vlaamscodex_autoload.pth  # Codec startup hook
│
├── vlaamscodex_build_backend.py  # Custom PEP 517 backend
├── pyproject.toml             # Package configuration
│
├── tests/                     # pytest test suite
├── examples/                  # Sample .plats programs
├── docs/                      # Documentation
│   ├── architecture/          # System design
│   ├── api/                   # API reference
│   └── technical/             # This directory
│
└── vscode-extension/          # VS Code extension (TypeScript)
```

### Key Technical Concepts

1. **Token-based Transpilation**: Simple line-by-line parsing, not AST-based
2. **Python Codec System**: Intercepts source encoding for magic mode
3. **PEP 517 Build Backend**: Custom wheel post-processing for .pth injection
4. **Rule-based Transformation**: JSON dialect packs with inheritance
5. **Protected Terms**: Legal/modality words exempt from transformation

### Development Commands

```bash
# Setup
pip install -e ".[dev]"

# Test
pytest tests/ -v
pytest tests/test_compiler.py -v  # Specific file

# Build
python -m build

# Validate dialect packs
python tools/validate_dialect_packs.py

# Run examples
plats run examples/hello.plats
python examples/hello.plats  # Magic mode
```
