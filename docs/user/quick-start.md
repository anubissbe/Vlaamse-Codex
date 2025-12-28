# Quick Start Guide

> Get VlaamsCodex running in 5 minutes!

## Step 1: Install

```bash
pip install vlaamscodex
```

Verify installation:

```bash
plats version
# VlaamsCodex v0.2.0
```

## Step 2: Your First Program

Create a file called `hallo.plats`:

```platskript
# coding: vlaamsplats
plan doe
  klap tekst gdag weeireld amen
gedaan
```

## Step 3: Run It!

**Option A: CLI Command**

```bash
plats run hallo.plats
```

**Option B: Magic Mode**

```bash
python hallo.plats
```

**Output:**
```
gdag weeireld
```

## Step 4: Try the REPL

Start an interactive session:

```bash
plats repl
```

```
🧇 Platskript REPL (type 'stop' om te stoppen)
>>> klap tekst hallo amen
hallo
>>> zet x op getal 5 amen
>>> klap da x amen
5
>>> stop
👋 Tot ziens!
```

## Step 5: Browse Examples

```bash
# List all examples
plats examples

# View an example
plats examples --show hello

# Run an example
plats examples --run hello
```

## Step 6: Use Your Dialect!

Every command has dialect aliases:

| Region | Run | REPL | Examples |
|--------|-----|------|----------|
| West-Vlaams | `voertuut` | `proboir` | `tuuntnekeer` |
| Antwerps | `doet` | `smos` | `toondada` |
| Limburgs | `gaon` | `efkes` | `loatskiejn` |
| Brussels | `doeda` | `klansen` | `toonmansen` |

Example:

```bash
# Antwerps style
smos                          # Start REPL
doet examples/hello.plats     # Run a file
toondada examples/hello.plats # Show generated Python
```

## Step 7: Create a Project

```bash
plats init myproject
cd myproject
plats run hallo.plats
```

Creates:
```
myproject/
├── hallo.plats      # Sample program
└── LEESMIJ.md       # Quick start guide
```

## What's Next?

- **[Language Tutorial](language-tutorial.md)**: Learn all Platskript syntax
- **[CLI Reference](cli-reference.md)**: All commands and options
- **[Dialect Guide](dialect-guide.md)**: Transform text to Flemish dialects

---

## Quick Reference Card

### Program Structure

```platskript
plan doe
  <statements>
gedaan
```

### Statements

```platskript
zet x op getal 10 amen              # Variable assignment
klap tekst hello amen               # Print
roep greet met tekst world amen     # Function call
geeftterug da x amen                # Return
```

### Functions

```platskript
maak funksie greet met name doe
  klap tekst hello plakt spatie plakt da name amen
gedaan
```

### Expressions

| Syntax | Description |
|--------|-------------|
| `tekst hello world` | String literal |
| `getal 42` | Number literal |
| `da x` | Variable reference |
| `spatie` | Space character |
| `plakt` | String concatenation |
| `derbij`, `deraf`, `keer`, `gedeeld` | Math operators |

---

**Veel plansen!** 🧇
