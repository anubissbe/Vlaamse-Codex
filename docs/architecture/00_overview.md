# VlaamsCodex Architecture Overview

This document provides a high-level view of the VlaamsCodex system architecture.

## System Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VlaamsCodex Toolchain                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────┐     ┌──────────────────────┐                     │
│  │   Platskript Files   │     │   Dutch/Flemish Text │                     │
│  │      (.plats)        │     │      (any text)      │                     │
│  └──────────┬───────────┘     └──────────┬───────────┘                     │
│             │                            │                                  │
│             ▼                            ▼                                  │
│  ┌──────────────────────┐     ┌──────────────────────┐                     │
│  │   Platskript → Python │     │  Dialect Transformer │                     │
│  │      Transpiler       │     │   (Text → Dialect)   │                     │
│  │  (compiler.py/codec)  │     │  (dialects/*)        │                     │
│  └──────────┬───────────┘     └──────────┬───────────┘                     │
│             │                            │                                  │
│             ▼                            ▼                                  │
│  ┌──────────────────────┐     ┌──────────────────────┐                     │
│  │    Python Source     │     │   Dialect-Flavored   │                     │
│  │       (exec)         │     │        Text          │                     │
│  └──────────────────────┘     └──────────────────────┘                     │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     Multi-Dialect CLI (cli.py)                        │  │
│  │  run | repl | check | init | examples | fortune | build | help       │  │
│  │  80+ dialect aliases from 7 Flemish regions                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    VS Code Extension                                  │  │
│  │  Syntax highlighting | Snippets | Commands                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Two Independent Subsystems

VlaamsCodex contains **two distinct but complementary subsystems**:

### 1. Platskript Transpiler

Converts Platskript (`.plats`) source code into executable Python.

| Component | Location | Purpose |
|-----------|----------|---------|
| Compiler | `src/vlaamscodex/compiler.py` | Token-based Platskript → Python transpilation |
| Codec | `src/vlaamscodex/codec.py` | Python source encoding for "magic mode" |
| Startup Hook | `data/vlaamscodex_autoload.pth` | Auto-registers codec at interpreter startup |
| Build Backend | `vlaamscodex_build_backend.py` | Custom PEP 517 backend for .pth injection |

### 2. Dialect Transformer

Rule-based text transformation system that applies Flemish dialect styling to text.

| Component | Location | Purpose |
|-----------|----------|---------|
| Transformer Engine | `src/vlaamscodex/dialects/transformer.py` | Core transformation logic |
| Dialect Registry | `dialects/index.json` | Pack metadata and inheritance |
| Dialect Packs | `dialects/packs/*.json` | Per-dialect transformation rules |
| Validation Tool | `tools/validate_dialect_packs.py` | Schema and consistency checks |
| Generation Tool | `tools/generate_dialect_packs.py` | Scaffold new packs |

## Directory Structure

```
Vlaamse-Codex/
├── src/vlaamscodex/           # Python package
│   ├── __init__.py            # Version and exports
│   ├── cli.py                 # Multi-dialect CLI router
│   ├── compiler.py            # Platskript → Python transpiler
│   ├── codec.py               # Python source encoding
│   ├── repl.py                # Interactive REPL
│   ├── checker.py             # Syntax validation
│   ├── examples.py            # Example browser
│   ├── fortune.py             # Proverb easter egg
│   ├── init.py                # Project scaffolding
│   └── dialects/              # Dialect transformer module
│       ├── __init__.py
│       └── transformer.py     # Core transformation engine
│
├── dialects/                  # Dialect pack data (separate from code)
│   ├── index.json             # Pack registry
│   ├── packs/                 # 83+ dialect JSON files
│   ├── README.md              # Pack documentation
│   └── schema.md              # Pack format specification
│
├── tools/                     # Development utilities
│   ├── validate_dialect_packs.py
│   └── generate_dialect_packs.py
│
├── data/                      # Package data files
│   └── vlaamscodex_autoload.pth
│
├── vscode-extension/          # VS Code extension (TypeScript)
│   ├── src/extension.ts       # Extension entry point
│   ├── syntaxes/              # TextMate grammar
│   └── snippets/              # Code snippets
│
├── examples/                  # Sample .plats programs
├── tests/                     # pytest test suite
└── docs/                      # Documentation
```

## Data Flow

### Platskript Execution

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  .plats     │───▶│   Codec     │───▶│   Python    │───▶│  Execution  │
│   file      │    │  (decode)   │    │   source    │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │
       │           ┌──────┴──────┐
       │           │  compiler   │
       │           │ .compile_   │
       │           │  plats()    │
       │           └─────────────┘
       │
 Via encoding cookie:
 # coding: vlaamsplats
```

### Dialect Transformation

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Input     │───▶│    Mask     │───▶│   Apply     │───▶│   Unmask    │
│   text      │    │  protected  │    │   rules     │    │  & return   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                  │
                   ┌──────┴──────┐    ┌──────┴──────┐
                   │  Legal/     │    │  Inherited  │
                   │  modality   │    │  rules from │
                   │  terms      │    │  pack chain │
                   └─────────────┘    └─────────────┘
```

## Key Design Decisions

### 1. Token-Based Transpilation (not AST)

The Platskript compiler uses simple token parsing rather than a full AST. This is intentional for a parody language—keeps complexity low while being sufficient for the feature set.

### 2. Codec-Based Magic Mode

Python's source encoding mechanism is leveraged to enable `python script.plats` execution. This requires early codec registration via `.pth` startup hook.

### 3. Rule-Based Dialect Transformation

Dialect packs use declarative JSON rules rather than code. This enables:
- Safe, sandboxed transformations
- Easy community contributions
- Inheritance chains for dialect families
- Protected terms to preserve legal/modality meaning

### 4. Separation of Code and Data

Dialect packs (`dialects/`) are separate from the Python package (`src/`). This allows:
- Independent versioning of language data
- Potential runtime loading of custom packs
- Clear separation of concerns

## Related Documentation

- [Platskript Transpiler](./01_transpiler.md) - Detailed transpiler architecture
- [Dialect Transformer](./02_dialect_transformer.md) - Transformation engine internals
- [CLI Architecture](./03_cli.md) - Command routing and dialect detection
- [Language Spec](../04_language_spec.md) - Platskript v0.1 specification
