# checker.py - Syntax Validation

> `src/vlaamscodex/checker.py`

Syntax checker for Platskript with multi-dialect error messages.

## Overview

The checker validates Platskript source code for common issues and returns errors in the user's preferred Flemish dialect.

## Functions

### `check_syntax(source: str, dialect: str = "default") -> list[SyntaxIssue]`

Check Platskript source code for common issues.

**Parameters:**
- `source` (str): Platskript source code
- `dialect` (str): Dialect for error messages ("default", "west-vlaams", "antwerps", etc.)

**Returns:**
- `list[SyntaxIssue]`: List of issues found

**Example:**
```python
from vlaamscodex.checker import check_syntax

source = """
plan doe
  klap tekst hallo
gedaan
"""

issues = check_syntax(source, dialect="antwerps")
for issue in issues:
    print(f"Line {issue.line_number}: {issue.message}")
    # Output: Manneke, gij zijt 'amen' vergeten!
```

---

### `check_file(path: Path, dialect: str = "default") -> tuple[bool, str]`

Check a Platskript file for syntax issues.

**Parameters:**
- `path` (Path): Path to `.plats` file
- `dialect` (str): Dialect for error messages

**Returns:**
- `tuple[bool, str]`: (success, message)

**Example:**
```python
from pathlib import Path
from vlaamscodex.checker import check_file

success, message = check_file(Path("script.plats"), dialect="limburgs")
print(message)
```

---

### `format_issues(issues: list[SyntaxIssue], path: str | None = None) -> str`

Format syntax issues for display.

**Parameters:**
- `issues` (list[SyntaxIssue]): Issues to format
- `path` (str, optional): File path for header

**Returns:**
- `str`: Formatted output string

---

### `get_error_message(error_type: str, dialect: str = "default") -> str`

Get a localized error message.

**Parameters:**
- `error_type` (str): Error type key
- `dialect` (str): Target dialect

**Returns:**
- `str`: Localized error message

---

### `get_success_message(dialect: str = "default") -> str`

Get a localized success message.

---

### `detect_checker_dialect(command: str) -> str`

Detect dialect from CLI command alias.

---

## Data Classes

### `SyntaxIssue`

Represents a syntax issue found during checking.

```python
@dataclass
class SyntaxIssue:
    line_number: int
    line_content: str
    issue_type: str
    message: str
    suggestion: str | None = None
```

---

## Error Types

| Type | Description |
|------|-------------|
| `missing_amen` | Statement missing 'amen' terminator |
| `missing_gedaan` | Block not closed with 'gedaan' |
| `missing_plan_doe` | Program doesn't start with 'plan doe' |
| `unbalanced_blocks` | Mismatched block openers/closers |
| `invalid_statement` | Unrecognized statement pattern |
| `empty_program` | No code to check |

---

## Dialect Error Messages

Each error type has messages in 7 dialects:

```python
ERROR_MESSAGES = {
    "missing_amen": {
        "default": "Missing 'amen' at end of statement",
        "west-vlaams": "Vergeten 'amen' te zetten, jong!",
        "antwerps": "Manneke, gij zijt 'amen' vergeten!",
        "limburgs": "Efkes nog 'amen' derbij zetten, hè?",
        "oost-vlaams": "Allez, 'amen' vergeten!",
        "brussels": "Eh, 'amen' oublié, sjongen!",
        "genks": "Jaow, 'amen' vergeten!",
    },
    # ... more error types
}
```

---

## CLI Aliases

| Dialect | Command |
|---------|---------|
| Default | `plats check` |
| West-Vlaams | `plats zijdezekers` |
| Antwerps | `plats istdagoe` |
| Limburgs | `plats kloptda` |
| Oost-Vlaams | `plats zalkdagaan` |
| Brussels | `plats passedat` |
| Genks | `plats jaowklopt` |

---

## Checks Performed

1. **Program structure**: `plan doe ... gedaan` wrapper
2. **Statement terminators**: `amen` at end of statements
3. **Block balance**: Matching openers and closers
4. **Function syntax**: `maak funksie ... doe` pattern
