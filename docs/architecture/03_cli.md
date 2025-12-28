# CLI Architecture

The VlaamsCodex CLI (`plats`) supports 80+ command aliases from 7 Flemish dialect regions, all routing to a common set of base commands.

## Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            CLI Router (cli.py)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  User Input ──▶ COMMAND_ALIASES ──▶ Base Command ──▶ Module Handler     │
│                                                                          │
│  Examples:                                                               │
│    plats run        ─┐                                                   │
│    plats loop       ─┼──▶ "run" ──▶ run_command()                       │
│    plats voertuut   ─┤                                                   │
│    plats doet       ─┤                                                   │
│    plats gaon       ─┘                                                   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Command Modules                               │    │
│  ├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤    │
│  │   repl.py   │ checker.py  │ examples.py │ fortune.py  │ init.py │    │
│  └─────────────┴─────────────┴─────────────┴─────────────┴─────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Command Routing

### COMMAND_ALIASES Dictionary

The `COMMAND_ALIASES` dict in `cli.py` maps every dialect alias to a base command:

```python
COMMAND_ALIASES = {
    # Run command
    "run": "run",
    "loop": "run",        # Flemish
    "voertuut": "run",    # West-Vlaams
    "doet": "run",        # Antwerps
    "gaon": "run",        # Limburgs
    "doeda": "run",       # Brussels
    "jaowdoen": "run",    # Genks

    # REPL command
    "repl": "repl",
    "proboir": "repl",    # West-Vlaams
    "smos": "repl",       # Antwerps
    "efkes": "repl",      # Limburgs
    "praot": "repl",      # Brussels

    # ... 80+ more aliases
}
```

### Base Commands

| Base Command | Purpose | Handler |
|--------------|---------|---------|
| `run` | Execute a .plats file | `run_command()` in cli.py |
| `repl` | Interactive REPL | `repl.py:run_repl()` |
| `check` | Syntax validation | `checker.py:check_file()` |
| `examples` | Browse examples | `examples.py:examples_command()` |
| `init` | Create new project | `init.py:init_project()` |
| `fortune` | Random proverb | `fortune.py:fortune_command()` |
| `build` | Compile to .py | `build_command()` in cli.py |
| `show-python` | Display compiled Python | in cli.py |
| `help` | Show help | argparse built-in |

## Module Pattern

Each command module follows a consistent pattern:

### 1. Dialect Alias Dictionary

```python
# In repl.py
REPL_ALIASES = {
    "repl": "repl",
    "proboir": "west-vlaams",
    "smos": "antwerps",
    "efkes": "limburgs",
    "praot": "brussels",
    "babbel": "genks",
}
```

### 2. Dialect Detection Function

```python
def detect_repl_dialect(used_alias: str) -> str | None:
    """Returns dialect name for localized messaging."""
    return REPL_ALIASES.get(used_alias)
```

### 3. Main Implementation

```python
def run_repl(dialect: str | None = None):
    """Run interactive REPL with optional dialect-specific prompts."""
    # Implementation...
```

## Dialect Regions

The CLI supports 7 Flemish dialect regions:

| Region | Example Alias | Characteristic |
|--------|---------------|----------------|
| West-Vlaams | `voertuut`, `proboir` | Coastal/western |
| Antwerps | `doet`, `smos` | Antwerp city |
| Limburgs | `gaon`, `efkes` | Eastern/Limburg |
| Brussels | `doeda`, `praot` | Brussels urban |
| Genks | `jaowdoen`, `babbel` | Genk-specific |
| Oost-Vlaams | various | East Flanders |
| Brabants | various | Brabant region |

## Error Message Localization

When errors occur, the CLI detects which dialect alias was used and returns errors in that dialect:

```python
def check_file(filepath: str, dialect: str | None = None):
    # On error, use dialect-specific message
    if dialect == "antwerps":
        print(f"Manneke, gij zijt 'amen' vergeten op lijn {line}!")
    elif dialect == "west-vlaams":
        print(f"Jansen, ge zijt 'amen' vergeten op lijn {line}!")
    else:
        print(f"Missing 'amen' on line {line}")
```

## Entry Point

### pyproject.toml Configuration

```toml
[project.scripts]
plats = "vlaamscodex.cli:main"
```

### main() Function

```python
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Register all aliases
    for alias in COMMAND_ALIASES:
        # Create subparser for each alias
        ...

    args = parser.parse_args()

    # Route to base command
    base_command = COMMAND_ALIASES.get(args.command, args.command)

    # Dispatch to handler
    if base_command == "run":
        run_command(args, used_alias=args.command)
    elif base_command == "repl":
        run_repl(detect_repl_dialect(args.command))
    # ... etc
```

## Adding New Commands

### 1. Create Module (if needed)

```python
# src/vlaamscodex/newcmd.py

NEWCMD_ALIASES = {
    "newcmd": "newcmd",
    "niece": "west-vlaams",    # Dialect variant
    "neukes": "antwerps",      # Dialect variant
}

def detect_newcmd_dialect(alias: str) -> str | None:
    return NEWCMD_ALIASES.get(alias)

def newcmd_handler(args, dialect: str | None = None):
    # Implementation
    pass
```

### 2. Update COMMAND_ALIASES

```python
# In cli.py
COMMAND_ALIASES = {
    ...
    # New command
    "newcmd": "newcmd",
    "niece": "newcmd",
    "neukes": "newcmd",
}
```

### 3. Wire into main()

```python
# In cli.py main()
elif base_command == "newcmd":
    from vlaamscodex.newcmd import newcmd_handler, detect_newcmd_dialect
    newcmd_handler(args, detect_newcmd_dialect(args.command))
```

### 4. Add to argparser

```python
# Create subparser with appropriate options
newcmd_parser = subparsers.add_parser("newcmd", ...)
newcmd_parser.add_argument("--option", ...)

# Also add for each alias
for alias in ["niece", "neukes"]:
    subparsers.add_parser(alias, ...)
```

## Files

| File | Purpose |
|------|---------|
| `src/vlaamscodex/cli.py` | Main CLI router and entry point |
| `src/vlaamscodex/repl.py` | Interactive REPL implementation |
| `src/vlaamscodex/checker.py` | Syntax validation |
| `src/vlaamscodex/examples.py` | Example browser |
| `src/vlaamscodex/fortune.py` | Proverb easter egg |
| `src/vlaamscodex/init.py` | Project scaffolding |

## VS Code Extension Integration

The VS Code extension shells out to the `plats` CLI:

```typescript
// In extension.ts
const terminal = vscode.window.createTerminal('Platskript');
terminal.sendText(`plats run ${filePath}`);
```

This allows the extension to leverage all CLI functionality without reimplementing it in TypeScript.
