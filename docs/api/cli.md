# cli.py - Multi-Dialect CLI

> `src/vlaamscodex/cli.py`

Command-line interface with 80+ dialect command aliases.

## Overview

The CLI routes dialect-specific command aliases to base commands, providing a localized experience for users from different Flemish regions.

## Functions

### `main() -> int`

Main CLI entry point. Parses arguments and dispatches to command handlers.

**Returns:**
- `int`: Exit code (0 = success)

**Entry point**: `plats` command (defined in `pyproject.toml`)

---

## Commands

| Base Command | Purpose | Handler |
|--------------|---------|---------|
| `run` | Execute a .plats file | `run_command()` |
| `repl` | Interactive REPL | `repl.run_repl()` |
| `check` | Syntax validation | `checker.check_file()` |
| `examples` | Browse examples | `examples.list_examples()` |
| `init` | Create new project | `init.create_project()` |
| `fortune` | Random proverb | `fortune.print_fortune()` |
| `build` | Compile to .py | `build_command()` |
| `show-python` | Display compiled Python | inline |
| `help` | Show help | argparse |

---

## Constants

### `COMMAND_ALIASES`

Dictionary mapping all dialect aliases to base commands.

```python
COMMAND_ALIASES = {
    # Run command (11+ aliases)
    "run": "run",
    "loop": "run",        # West-Vlaams
    "voertuut": "run",    # West-Vlaams
    "doet": "run",        # Antwerps
    "gaon": "run",        # Limburgs
    "doeda": "run",       # Brussels
    "jaowdoen": "run",    # Genks

    # REPL command
    "repl": "repl",
    "proboir": "repl",    # West-Vlaams
    "smos": "repl",       # Antwerps

    # ... 80+ total aliases
}
```

---

## Dialect Regions

| Region | Example Aliases |
|--------|-----------------|
| West-Vlaams | `loop`, `proboir`, `tuuntnekeer` |
| Antwerps | `doet`, `smos`, `toondada` |
| Limburgs | `gaon`, `efkes`, `loatskiejn` |
| Oost-Vlaams | `doeme`, `komaan`, `ziedievoorbeelden` |
| Brussels | `doeda`, `praot`, `toontmansen` |
| Genks | `jaowdoen`, `babbel`, `jaowkiek` |
| Vlaams-Brabants | `startdansen`, `zegansen` |

---

## Usage Examples

```bash
# Run a script
plats run script.plats
plats loop script.plats      # West-Vlaams
plats doet script.plats      # Antwerps

# Start REPL
plats repl
plats proboir                 # West-Vlaams
plats smos                    # Antwerps

# Check syntax
plats check script.plats
plats zijdezekers script.plats  # West-Vlaams

# Initialize project
plats init myproject
plats allehop mijnproject     # West-Vlaams

# Show examples
plats examples
plats tuuntnekeer             # West-Vlaams

# Get a fortune
plats fortune
plats zegt                    # West-Vlaams
```

---

## Adding New Commands

1. **Create command module** with dialect aliases:
   ```python
   # newcmd.py
   NEWCMD_ALIASES = {
       "newcmd": "newcmd",
       "nieuwe": "west-vlaams",
   }

   def detect_newcmd_dialect(alias: str) -> str | None:
       return NEWCMD_ALIASES.get(alias)

   def newcmd_handler(args, dialect: str | None = None):
       pass
   ```

2. **Update COMMAND_ALIASES** in `cli.py`

3. **Wire into main()** dispatcher

4. **Add argparser subparsers** for all aliases

See: [Architecture: CLI](../architecture/03_cli.md)
