# fortune.py - Proverb Easter Egg

> `src/vlaamscodex/fortune.py`

Random Flemish proverbs and programmer humor.

## Overview

Displays random Flemish wisdom from 6 dialect regions plus programmer jokes.

## Functions

### `get_fortune(dialect: str | None = None) -> str`

Get a random Flemish fortune.

**Parameters:**
- `dialect` (str, optional): Filter by dialect region

**Returns:**
- `str`: Random fortune string

**Example:**
```python
from vlaamscodex.fortune import get_fortune

# Random from all dialects
print(get_fortune())

# West-Vlaams only
print(get_fortune("west-vlaams"))
```

---

### `print_fortune(dialect: str | None = None) -> int`

Print a formatted fortune with decorative box.

**Parameters:**
- `dialect` (str, optional): Dialect filter

**Returns:**
- `int`: Exit code (always 0)

**Output:**
```
  ══════════════════════════════════════════
  ║ 'plan doe' zei ik, 'gedaan' zeg ik nu ║
  ══════════════════════════════════════════

        - Vlaamse wijsheid 🇧🇪
```

---

### `detect_fortune_dialect(command: str) -> str | None`

Detect dialect from fortune command alias.

---

## Fortune Categories

### Regional Proverbs

| Region | Count | Example |
|--------|-------|---------|
| West-Vlaams | 15 | "'t Es simpel, 't es plansen, 't es Vlaams!" |
| Antwerps | 15 | "Ge moet uwe plan trekken, manneke!" |
| Limburgs | 15 | "Allei, da geit waal good komme!" |
| Brussels | 15 | "Une fois, deux fois, de code marche!" |
| Oost-Vlaams | 15 | "Allez, da's rap gedaan!" |
| Genks | 15 | "Jaow, da werkt!" |

### Programmer Humor

15 programming-related jokes in Flemish:
- "99 bugs op den stack... fix er een... 127 bugs op den stack!"
- "'t Werkt op mijn machine! - beroemde laatste woorden"

### Special Fortunes

5 seasonal/themed fortunes with emojis.

---

## CLI Aliases

| Dialect | Command |
|---------|---------|
| Default | `plats fortune` |
| West-Vlaams | `plats zegt`, `plats zenmoederzegt` |
| Antwerps | `plats watteda`, `plats manneke` |
| Limburgs | `plats wiste`, `plats wistedak` |
| Brussels | `plats zansen` |
| Oost-Vlaams | `plats spreuk` |
| Genks | `plats jaow` |

---

## Constants

### `FORTUNE_ALIASES`

Mapping of dialect command aliases.

### `ALL_FORTUNES`

Combined tuple of all fortune strings (90+ total).
