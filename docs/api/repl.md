# repl.py - Interactive REPL

> `src/vlaamscodex/repl.py`

Interactive Read-Eval-Print Loop for Platskript with dialect-aware prompts.

## Overview

The REPL allows interactive execution of Platskript code with multi-line support and dialect-specific messaging.

## Functions

### `run_repl(dialect: str | None = None) -> int`

Run the interactive REPL.

**Parameters:**
- `dialect` (str, optional): Dialect for prompts and messages

**Returns:**
- `int`: Exit code (always 0)

**Example:**
```bash
$ plats repl
🇧🇪 Platskript REPL
Type 'stop' or Ctrl+D to exit

>>> klap tekst hallo amen
hallo
>>>
```

---

### `detect_repl_dialect(used_alias: str) -> str | None`

Detect dialect from REPL command alias.

**Parameters:**
- `used_alias` (str): Command used to invoke REPL

**Returns:**
- `str | None`: Dialect name or None

---

## Constants

### `REPL_ALIASES`

Mapping of dialect command aliases.

```python
REPL_ALIASES = {
    "repl": "repl",
    "proboir": "west-vlaams",
    "smos": "antwerps",
    "efkes": "limburgs",
    "praot": "brussels",
    "babbel": "genks",
}
```

---

## CLI Aliases

| Dialect | Command |
|---------|---------|
| Default | `plats repl` |
| West-Vlaams | `plats proboir` |
| Antwerps | `plats smos` |
| Limburgs | `plats efkes` |
| Brussels | `plats praot` |
| Genks | `plats babbel` |

---

## Features

- **Multi-line input**: Use `...` continuation for blocks
- **Dialect prompts**: Localized prompt messages
- **Error handling**: Graceful error display
- **Exit commands**: `stop`, `quit`, `exit`, or Ctrl+D

---

## REPL Session Example

```
$ plats smos  # Antwerps dialect
🇧🇪 Platskript REPL (Antwerps stansen!)
Manneke, type 'stop' om te stoppen

>>> zet x op getal 10 amen
>>> klap da x amen
10
>>> maak funksie groet met naam doe
...   klap tekst hallo plakt spatie plakt da naam amen
... gedaan
>>> roep groet met tekst manneke amen
hallo manneke
>>> stop
Salut, manneke!
```
