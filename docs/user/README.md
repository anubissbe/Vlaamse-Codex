# User Documentation

> Complete guides for using VlaamsCodex and Platskript.

## Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](quick-start.md) | Get running in 5 minutes |
| [CLI Reference](cli-reference.md) | All commands and dialect aliases |
| [Language Tutorial](language-tutorial.md) | Learn Platskript step-by-step |
| [Dialect Guide](dialect-guide.md) | Multi-Vlaams text transformation |
| [Troubleshooting](troubleshooting.md) | Common issues and solutions |

## What is VlaamsCodex?

VlaamsCodex is a fun, parody programming language that uses **Flemish dialect keywords**. It transpiles to Python and runs anywhere Python runs.

```platskript
# coding: vlaamsplats
plan doe
  klap tekst gdag weeireld amen
gedaan
```

Output: `gdag weeireld`

## Key Features

- **Platskript Language**: Write code in Flemish dialect
- **Magic Mode**: Run `.plats` files directly with `python script.plats`
- **Multi-Vlaams CLI**: 80+ command aliases from 7 Flemish regions
- **Dialect Transformer**: Convert Dutch text to regional dialects
- **Interactive REPL**: Experiment with code live
- **VS Code Extension**: Syntax highlighting and snippets

## Installation

```bash
pip install vlaamscodex
```

Then start coding:

```bash
plats run examples/hello.plats
```

Or use dialect commands:

```bash
# West-Vlaams
voertuut examples/hello.plats

# Antwerps
doet examples/hello.plats

# Limburgs
gaon examples/hello.plats
```

---

**'t Es simpel, 't es plansen!**
