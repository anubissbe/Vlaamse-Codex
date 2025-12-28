# init.py - Project Scaffolding

> `src/vlaamscodex/init.py`

Create new Platskript projects with starter templates.

## Overview

Scaffolds a new project directory with a sample `.plats` program and Flemish README.

## Functions

### `create_project(name: str, dialect: str = "default") -> int`

Create a new Platskript project.

**Parameters:**
- `name` (str): Project name (used as directory name)
- `dialect` (str): Dialect for welcome message

**Returns:**
- `int`: Exit code (0 = success, 1 = error)

**Example:**
```python
from vlaamscodex.init import create_project

# Create with English welcome
create_project("myproject")

# Create with West-Vlaams welcome
create_project("mijnproject", dialect="west-vlaams")
```

**Created structure:**
```
myproject/
├── hallo.plats    # Sample Platskript program
└── LEESMIJ.md     # Quick start guide (in Flemish)
```

---

### `detect_init_dialect(command: str) -> str`

Detect dialect from init command alias.

---

### `print_init_help() -> int`

Print help for init command.

---

## CLI Aliases

| Dialect | Command |
|---------|---------|
| Default | `plats init <name>` |
| West-Vlaams | `plats allehop <name>` |
| Antwerps | `plats awel <name>` |
| Limburgs | `plats allei <name>` |
| Oost-Vlaams | `plats komaan <name>` |
| Brussels | `plats allez <name>` |
| Genks | `plats jaowel <name>` |

---

## Templates

### `HELLO_PLATS`

Sample program created as `hallo.plats`:

```platskript
# coding: vlaamsplats
# 🇧🇪 Uw eerste Platskript programma!

plan doe
  zet naam op tekst weeireld amen

  maak funksie groet met wie doe
    klap tekst gdag plakt spatie plakt tekst aan plakt spatie plakt da wie amen
  gedaan

  roep groet met da naam amen
gedaan
```

### `LEESMIJ_MD`

Flemish README with:
- Quick start instructions
- Dialect command examples
- Syntax reference table
- Useful commands
- Links to documentation

---

## Welcome Messages

Localized project creation messages:

| Dialect | Message |
|---------|---------|
| West-Vlaams | "Allehop! Uw project is aangemaakt!" |
| Antwerps | "Awel manneke! Uw project is aangemaakt!" |
| Limburgs | "Allei! Uw project is aangemaakt!" |
| Oost-Vlaams | "Komaan! Uw project is aangemaakt!" |
| Brussels | "Allez! Uw project est aangemaakt!" |
| Genks | "Jaow! Uw project is aangemaakt!" |

---

## Usage

```bash
# Create new project
plats init myproject
cd myproject
plats run hallo.plats

# With dialect
plats allehop mijnproject  # West-Vlaams
```
