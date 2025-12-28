# Project Index: VlaamsCodex

> **Generated**: 2024-12-28 | **Version**: 0.2.0 | **Python**: >=3.10 | **Docs**: 39 files

A transpiler toolchain for **Platskript** (`.plats`), a parody programming language using Flemish dialect keywords that compiles to Python.

---

## Quick Navigation

| Category | Purpose | Start Here |
|----------|---------|------------|
| [Architecture](#-architecture-docs) | System design & decisions | [00_overview.md](docs/architecture/00_overview.md) |
| [API Reference](#-api-reference) | Module documentation | [README.md](docs/api/README.md) |
| [User Guide](#-user-documentation) | Installation & tutorials | [quick-start.md](docs/user/quick-start.md) |
| [Admin/Ops](#-admin--operations) | Releases & maintenance | [README.md](docs/admin/README.md) |
| [Technical](#-technical-documentation) | Internals & testing | [README.md](docs/technical/README.md) |
| [Dialects](#-dialect-packs) | 84 transformation packs | [README.md](dialects/README.md) |

---

## Project Structure

```
Vlaamse-Codex/
├── src/vlaamscodex/          # Python package (11 modules)
│   ├── cli.py                # Multi-dialect CLI entry point
│   ├── compiler.py           # Platskript → Python transpiler
│   ├── codec.py              # Python source encoding for magic mode
│   ├── repl.py               # Interactive REPL
│   ├── checker.py            # Syntax validation
│   ├── examples.py           # Example browser
│   ├── fortune.py            # Proverb easter egg
│   ├── init.py               # Project scaffolding
│   └── dialects/             # Dialect transformer subsystem
│       └── transformer.py    # Rule-based text transformation
│
├── dialects/                 # Dialect pack data (84 packs)
│   ├── index.json            # Pack registry
│   ├── packs/*.json          # Individual dialect rules
│   ├── README.md             # Pack documentation
│   └── schema.md             # Pack format specification
│
├── tools/                    # Development utilities
│   ├── validate_dialect_packs.py   # Schema validation
│   └── generate_dialect_packs.py   # Pack scaffolding
│
├── tests/                    # pytest test suite (4 files)
├── examples/                 # Sample .plats programs (5 files)
├── docs/                     # Documentation (39 files total)
│   ├── architecture/         # System architecture (4 files)
│   ├── api/                  # API reference (10 files)
│   ├── technical/            # Technical docs (6 files)
│   ├── user/                 # User guides (6 files)
│   └── admin/                # Operations docs (6 files)
├── vscode-extension/         # VS Code extension (TypeScript)
└── data/                     # Package data files
    └── vlaamscodex_autoload.pth
```

---

## Entry Points

| Entry | Path | Purpose |
|-------|------|---------|
| **CLI** | `src/vlaamscodex/cli.py:main` | `plats` command (80+ dialect aliases) |
| **Codec** | `src/vlaamscodex/codec.py:register` | Enables `python script.plats` |
| **Transformer** | `src/vlaamscodex/dialects/transformer.py:transform` | Dialect text transformation |

---

## Core Modules

### Transpiler Subsystem

| Module | Key Exports | Documentation |
|--------|-------------|---------------|
| `compiler.py` | `compile_plats()`, `OP_MAP` | [docs/api/compiler.md](docs/api/compiler.md) |
| `codec.py` | `register()`, `VlaamsPlatsCodec` | [docs/api/codec.md](docs/api/codec.md) |

### CLI Subsystem

| Module | Key Exports | Documentation |
|--------|-------------|---------------|
| `cli.py` | `main()`, `COMMAND_ALIASES` | [docs/api/cli.md](docs/api/cli.md) |
| `repl.py` | `run_repl()`, `REPL_ALIASES` | [docs/api/repl.md](docs/api/repl.md) |
| `checker.py` | `check_file()`, `check_syntax()` | [docs/api/checker.md](docs/api/checker.md) |
| `examples.py` | `list_examples()`, `run_example()` | [docs/api/examples.md](docs/api/examples.md) |
| `fortune.py` | `print_fortune()`, `PROVERBS` | [docs/api/fortune.md](docs/api/fortune.md) |
| `init.py` | `create_project()` | [docs/api/init.md](docs/api/init.md) |

### Dialect Transformer Subsystem

| Module | Key Exports | Documentation |
|--------|-------------|---------------|
| `dialects/transformer.py` | `transform()`, `available_packs()`, `PackInfo` | [docs/api/transformer.md](docs/api/transformer.md) |

---

## Documentation Map

### Root Documentation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Project introduction, quick start |
| [CLAUDE.md](CLAUDE.md) | AI assistant guidance (most current) |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

### Architecture Docs

System design and architectural decisions.

| File | Topic |
|------|-------|
| [00_overview.md](docs/architecture/00_overview.md) | System architecture overview |
| [01_transpiler.md](docs/architecture/01_transpiler.md) | Compiler & codec architecture |
| [02_dialect_transformer.md](docs/architecture/02_dialect_transformer.md) | Transformer engine design |
| [03_cli.md](docs/architecture/03_cli.md) | CLI command routing |

### API Reference

Module-by-module API documentation.

| File | Module | Key Functions |
|------|--------|---------------|
| [README.md](docs/api/README.md) | Index | Module navigation |
| [compiler.md](docs/api/compiler.md) | `compiler.py` | `compile_plats()`, `OP_MAP` |
| [codec.md](docs/api/codec.md) | `codec.py` | `register()`, magic mode |
| [transformer.md](docs/api/transformer.md) | `transformer.py` | `transform()`, `available_packs()` |
| [cli.md](docs/api/cli.md) | `cli.py` | `main()`, `COMMAND_ALIASES` |
| [checker.md](docs/api/checker.md) | `checker.py` | `check_syntax()`, `check_file()` |
| [repl.md](docs/api/repl.md) | `repl.py` | `run_repl()`, REPL modes |
| [examples.md](docs/api/examples.md) | `examples.py` | `list_examples()`, `run_example()` |
| [fortune.md](docs/api/fortune.md) | `fortune.py` | `print_fortune()`, `PROVERBS` |
| [init.md](docs/api/init.md) | `init.py` | `create_project()` |

### Technical Documentation

Build system, internals, and testing.

| File | Topic |
|------|-------|
| [README.md](docs/technical/README.md) | Technical docs index |
| [build-system.md](docs/technical/build-system.md) | PEP 517 backend, .pth injection |
| [transpiler-internals.md](docs/technical/transpiler-internals.md) | Token processing, OP_MAP |
| [dialect-engine.md](docs/technical/dialect-engine.md) | Transformation pipeline |
| [testing.md](docs/technical/testing.md) | Test strategy, fixtures |
| [contributing.md](docs/technical/contributing.md) | Development workflow |

### User Documentation

Installation, tutorials, and troubleshooting.

| File | Topic | Audience |
|------|-------|----------|
| [README.md](docs/user/README.md) | User docs index | All users |
| [quick-start.md](docs/user/quick-start.md) | 5-minute getting started | New users |
| [cli-reference.md](docs/user/cli-reference.md) | All 12 commands, 80+ aliases | All users |
| [language-tutorial.md](docs/user/language-tutorial.md) | 6 Platskript lessons | Learners |
| [dialect-guide.md](docs/user/dialect-guide.md) | Dialect transformation | Power users |
| [troubleshooting.md](docs/user/troubleshooting.md) | Common issues & solutions | All users |

### Admin & Operations

Release process, deployment, and maintenance.

| File | Topic |
|------|-------|
| [README.md](docs/admin/README.md) | Admin index + quick reference |
| [release-process.md](docs/admin/release-process.md) | Version sync, tagging, rollback |
| [deployment.md](docs/admin/deployment.md) | PyPI, VS Code Marketplace |
| [configuration.md](docs/admin/configuration.md) | 9 environment variables |
| [maintenance.md](docs/admin/maintenance.md) | Health checks, runbook |
| [ci-cd.md](docs/admin/ci-cd.md) | GitHub Actions workflows |

### Dialect Documentation

| File | Topic |
|------|-------|
| [README.md](dialects/README.md) | Dialect packs overview |
| [schema.md](dialects/schema.md) | Pack JSON format specification |

### Legacy Documentation

Older docs preserved for reference. May contain outdated information.

| File | Topic |
|------|-------|
| [01_overview.md](docs/01_overview.md) | Original overview |
| [02_how_python_runs_it.md](docs/02_how_python_runs_it.md) | Magic mode internals |
| [03_packaging_and_install.md](docs/03_packaging_and_install.md) | Packaging details |
| [04_language_spec.md](docs/04_language_spec.md) | Platskript v0.1 spec |
| [05_security_and_safety.md](docs/05_security_and_safety.md) | Security considerations |
| [06_user_guide.md](docs/06_user_guide.md) | Original user guide |
| [08_plats_documentation_en.md](docs/08_plats_documentation_en.md) | English documentation |

---

## Configuration

### Build & Package Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Package metadata, dependencies, CLI entry |
| `vlaamscodex_build_backend.py` | Custom PEP 517 backend for .pth injection |
| `data/vlaamscodex_autoload.pth` | Startup hook for codec registration |
| `MANIFEST.in` | Source distribution includes |

### CI/CD Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `.github/workflows/ci.yml` | Push/PR to main | Test Python 3.10-3.12 |
| `.github/workflows/publish.yml` | GitHub Release | Build & publish to PyPI |

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `VLAAMSCODEX_DIALECTS_DIR` | auto | Override dialect packs location |
| `VLAAMSCODEX_DIALECT_DETERMINISTIC` | `True` | Enable deterministic mode |
| `VLAAMSCODEX_DIALECT_SEED` | `0` | Seed for randomness |
| `VLAAMSCODEX_DIALECT_PARTICLES` | `False` | Enable particle insertion |
| `VLAAMSCODEX_DIALECT_MAX_PASSES` | `3` | Max transformation passes |
| `VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY` | `False` | Raise on non-convergence |
| `VLAAMSCODEX_PRONOUN_SUBJECT` | `ge` | Subject pronoun |
| `VLAAMSCODEX_PRONOUN_OBJECT` | `u` | Object pronoun |
| `VLAAMSCODEX_PRONOUN_POSSESSIVE` | `uw` | Possessive pronoun |

See [docs/admin/configuration.md](docs/admin/configuration.md) for full details.

---

## Test Coverage

| File | Tests | Topic |
|------|-------|-------|
| `tests/test_compiler.py` | 5 | Transpiler unit tests |
| `tests/test_magic_subprocess.py` | 2 | Magic mode integration |
| `tests/test_dialect_transformer.py` | 2 | Transformer tests |
| `tests/conftest.py` | - | Test fixtures |

**Run tests**: `pytest tests/ -v`

See [docs/technical/testing.md](docs/technical/testing.md) for test strategy.

---

## Data Assets

| Asset | Count | Location | Documentation |
|-------|-------|----------|---------------|
| Dialect packs | 84 | `dialects/packs/*.json` | [dialects/README.md](dialects/README.md) |
| Example programs | 5 | `examples/*.plats` | [docs/api/examples.md](docs/api/examples.md) |

### Example Programs

| File | Demonstrates |
|------|--------------|
| `hello.plats` | Basic output |
| `funksies.plats` | Function definitions |
| `teller.plats` | Counting loop |
| `begroeting.plats` | String operations |
| `rekenmachine.plats` | Arithmetic |

---

## VS Code Extension

| File | Purpose |
|------|---------|
| `vscode-extension/package.json` | Extension manifest |
| `vscode-extension/src/extension.ts` | TypeScript entry point |
| `vscode-extension/syntaxes/` | TextMate grammar |
| `vscode-extension/snippets/` | Code snippets |

**Build**: `cd vscode-extension && npm install && npm run compile && npx @vscode/vsce package`

---

## Development Tools

| Tool | Purpose |
|------|---------|
| `tools/validate_dialect_packs.py` | Validate dialect pack schema |
| `tools/generate_dialect_packs.py` | Scaffold new dialect packs |

---

## Quick Commands

```bash
# Install
pip install -e ".[dev]"

# Run a Platskript file
plats run examples/hello.plats

# Or use magic mode
python examples/hello.plats

# Start REPL
plats repl

# List dialects
plats dialecten

# Run tests
pytest tests/ -v

# Build package
python -m build

# Validate dialect packs
python tools/validate_dialect_packs.py

# Health check
plats version && python -c "import codecs; codecs.lookup('vlaamsplats')"
```

---

## Version Sync Points

Keep these in sync when releasing:

1. `src/vlaamscodex/__init__.py` → `__version__`
2. `pyproject.toml` → `project.version`
3. `vscode-extension/package.json` → `version`

See [docs/admin/release-process.md](docs/admin/release-process.md) for release procedure.

---

## Quick Lookup

### CLI Commands (12)

| Command | Aliases | Purpose |
|---------|---------|---------|
| `run` | `uitvoeren`, `stansen` | Execute .plats file |
| `repl` | `babbelen`, `klansen` | Interactive mode |
| `check` | `bezien`, `bekansen` | Syntax validation |
| `examples` | `voorbeelden` | Browse examples |
| `init` | `beginne` | Create project |
| `fortune` | `wijsheid` | Random proverb |
| `build` | `bouwen` | Compile to .py |
| `show-python` | `toon-python` | Show transpiled code |
| `dialecten` | `streektalen` | List dialects |
| `vraag` | `transform` | Transform text |
| `version` | `versie` | Show version |
| `help` | `hulp` | Show help |

### Dialect Regions (7)

| Region | Packs | Example |
|--------|-------|---------|
| West-Vlaams | 12 | `west-vlaams`, `brugs` |
| Antwerps | 12 | `antwerps`, `mechels` |
| Limburgs | 12 | `limburgs`, `hasselts` |
| Brussels | 12 | `brussels`, `marols` |
| Oost-Vlaams | 12 | `oost-vlaams`, `gents` |
| Brabants | 12 | `brabants`, `leuvens` |
| Algemeen | 12 | `algemeen-vlaams` |

### Platskript Syntax

| Element | Syntax | Example |
|---------|--------|---------|
| Statement end | `amen` | `klap tekst hello amen` |
| Block close | `gedaan` | `plan doe ... gedaan` |
| Variable ref | `da <name>` | `da x` |
| String literal | `tekst <words>` | `tekst hello world` |
| Number literal | `getal <n>` | `getal 42` |
| Print | `klap <expr>` | `klap da naam amen` |
| Assign | `zet <var> op <expr>` | `zet x op getal 10 amen` |
| Function | `maak funksie <name>` | `maak funksie greet met wie doe` |
| Call | `roep <func> met <args>` | `roep greet met tekst world amen` |
| Return | `geeftterug <expr>` | `geeftterug da x amen` |
| Concatenate | `plakt` | `tekst a plakt tekst b` |

---

## Documentation Statistics

| Category | Files | Path |
|----------|-------|------|
| Root | 4 | `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md` |
| Architecture | 4 | `docs/architecture/` |
| API Reference | 10 | `docs/api/` |
| Technical | 6 | `docs/technical/` |
| User | 6 | `docs/user/` |
| Admin | 6 | `docs/admin/` |
| Legacy | 7 | `docs/` (numbered files) |
| Dialects | 2 | `dialects/` |
| **Total** | **39** | |

---

*Last updated: 2024-12-28 | Generated by /sc:index*
