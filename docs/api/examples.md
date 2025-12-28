# examples.py - Example Browser

> `src/vlaamscodex/examples.py`

Browse and run built-in Platskript examples.

## Overview

Provides an interactive browser for built-in Platskript examples with dialect-aware output.

## Functions

### `list_examples(dialect: str = "default") -> None`

List all available examples.

**Parameters:**
- `dialect` (str): Dialect for headers

---

### `show_example(name: str) -> int`

Show the source code of an example.

**Parameters:**
- `name` (str): Example name (e.g., "hello", "rekenen")

**Returns:**
- `int`: Exit code (0 = success, 1 = not found)

---

### `run_example(name: str) -> int`

Run an example using InteractiveConsole.

**Parameters:**
- `name` (str): Example name

**Returns:**
- `int`: Exit code

---

### `save_example(name: str, path: Path | None = None) -> int`

Save an example to a file.

**Parameters:**
- `name` (str): Example name
- `path` (Path, optional): Output path (default: `<name>.plats`)

**Returns:**
- `int`: Exit code

---

### `detect_examples_dialect(command: str) -> str`

Detect dialect from command alias.

---

## Built-in Examples

| Name | Description |
|------|-------------|
| `hello` | Hello World - first program |
| `rekenen` | Calculator - basic arithmetic |
| `funksies` | Functions - def and call |
| `begroeting` | Greetings - string operations |
| `teller` | Counter - variable manipulation |

---

## CLI Aliases

| Dialect | Command |
|---------|---------|
| Default | `plats examples` |
| West-Vlaams | `plats tuuntnekeer` |
| Antwerps | `plats toondada` |
| Limburgs | `plats loatskiejn` |
| Oost-Vlaams | `plats ziedievoorbeelden` |
| Brussels | `plats toontmansen` |
| Genks | `plats jaowkiek` |

---

## Usage

```bash
# List all examples
plats examples

# Show example code
plats examples --show hello

# Run an example
plats examples --run rekenen

# Save to file
plats examples --save funksies

# Dialect variant
plats tuuntnekeer --run hello
```
