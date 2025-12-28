# Architecture Overview

> VlaamsCodex system design and component architecture 🏗️

This page provides a high-level view of VlaamsCodex's architecture, designed for developers who want to understand or contribute to the project.

---

## System Diagram

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

---

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

**See:** [[Transpiler-Internals]] for detailed documentation.

### 2. Dialect Transformer

Rule-based text transformation system that applies Flemish dialect styling to text.

| Component | Location | Purpose |
|-----------|----------|---------|
| Transformer Engine | `src/vlaamscodex/dialects/transformer.py` | Core transformation logic |
| Dialect Registry | `dialects/index.json` | Pack metadata and inheritance |
| Dialect Packs | `dialects/packs/*.json` | Per-dialect transformation rules |
| Validation Tool | `tools/validate_dialect_packs.py` | Schema and consistency checks |
| Generation Tool | `tools/generate_dialect_packs.py` | Scaffold new packs |

**See:** [[Dialect-Engine]] for detailed documentation.

---

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
│   ├── packs/                 # 84+ dialect JSON files
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

---

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

---

## Key Design Decisions

### 1. Token-Based Transpilation (not AST)

The Platskript compiler uses simple token parsing rather than a full AST. This is intentional for a parody language—keeps complexity low while being sufficient for the feature set.

**Trade-offs:**
- ✅ Simple implementation (~200 lines)
- ✅ Easy to understand and debug
- ❌ Limited grammar flexibility
- ❌ No nested expressions

**See:** [[Transpiler-Internals]] for details.

### 2. Codec-Based Magic Mode

Python's source encoding mechanism is leveraged to enable `python script.plats` execution. This requires early codec registration via `.pth` startup hook.

**How it works:**
1. `.pth` file executes at Python startup
2. Registers `vlaamsplats` codec
3. Python sees `# coding: vlaamsplats` in source file
4. Codec returns transpiled Python

**See:** [[Magic-Mode]] for implementation details.

### 3. Rule-Based Dialect Transformation

Dialect packs use declarative JSON rules rather than code. This enables:

- ✅ Safe, sandboxed transformations
- ✅ Easy community contributions
- ✅ Inheritance chains for dialect families
- ✅ Protected terms to preserve legal/modality meaning

### 4. Separation of Code and Data

Dialect packs (`dialects/`) are separate from the Python package (`src/`). This allows:

- Independent versioning of language data
- Potential runtime loading of custom packs
- Clear separation of concerns

---

## CLI Architecture

The CLI uses a command alias system for dialect support:

```python
COMMAND_ALIASES = {
    # Standard
    "run": "run",
    "repl": "repl",

    # West-Vlaams
    "voertuut": "run",
    "proboir": "repl",

    # Antwerps
    "doet": "run",
    "smos": "repl",

    # ... 80+ total aliases
}
```

Each command module follows a pattern:
- `*_ALIASES` dict for dialect mappings
- `detect_*_dialect()` function for error message localization
- Main implementation function

---

## VS Code Extension

The TypeScript extension provides:

| Component | Purpose |
|-----------|---------|
| TextMate Grammar | Syntax highlighting for `.plats` files |
| Snippets | Code completion for common patterns |
| Commands | Integration with `plats` CLI |

The extension shells out to the `plats` CLI for:
- Running programs
- Checking syntax
- Building to Python
- Starting REPL

---

## Version Management

Version is defined in three places that must stay in sync:

| Location | Field |
|----------|-------|
| `src/vlaamscodex/__init__.py` | `__version__` |
| `pyproject.toml` | `project.version` |
| `vscode-extension/package.json` | `version` |

---

## Build System

VlaamsCodex uses a custom PEP 517 build backend:

```
pyproject.toml → vlaamscodex_build_backend.py → setuptools → wheel
                         │
                         ├── Inject .pth file
                         └── Inject dialects/ directory
```

**See:** [[Build-and-Release]] for the complete build system documentation.

---

## Test Configuration

The `tests/conftest.py` handles a special requirement: since the package installs a `.pth` file that auto-imports `vlaamscodex` at interpreter startup, tests must force-reload the module from `src/` to test the development version.

---

## Security Considerations

1. **No code execution in dialect packs**: Packs are pure data (JSON rules)
2. **Protected terms**: Legal/modality words are immutable
3. **Bounded iteration**: `max_passes` prevents infinite loops
4. **Deterministic by default**: Reproducible transformations

---

## See Also

- [[Transpiler-Internals]] - How Platskript compiles to Python
- [[Dialect-Engine]] - Transformer engine internals
- [[Magic-Mode]] - Codec system and startup hook
- [[Build-and-Release]] - Build system details
- [[Contributing]] - Development workflow

---

**Veel plansen!** 🧇
