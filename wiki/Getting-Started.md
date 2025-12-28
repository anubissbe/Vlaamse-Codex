# Getting Started

> Get VlaamsCodex running in 5 minutes! 🚀

This guide will take you from zero to running your first Platskript program.

---

## Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package manager)

Check your Python version:

```bash
python --version
# Python 3.10.0 or higher
```

---

## Step 1: Install VlaamsCodex

### Option A: pip (Recommended)

```bash
pip install vlaamscodex
```

### Option B: pipx (Isolated)

```bash
pipx install vlaamscodex
```

### Option C: From Source (Development)

```bash
git clone https://github.com/brentishere41848/Vlaams-Codex.git
cd Vlaams-Codex
pip install -e ".[dev]"
```

---

## Step 2: Verify Installation

Run these commands to verify everything works:

```bash
# Check CLI is available
plats version
# VlaamsCodex v0.2.0

# Check codec is registered (for magic mode)
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
# <codecs.CodecInfo object ...>
```

If either command fails, see [[Troubleshooting]].

---

## Step 3: Your First Program

Create a file called `hallo.plats`:

```platskript
# coding: vlaamsplats
plan doe
  klap tekst gdag weeireld amen
gedaan
```

### Understanding the Code

| Code | Meaning |
|------|---------|
| `# coding: vlaamsplats` | Tells Python to use the VlaamsCodex codec |
| `plan doe` | "Plan do" - Start of the program |
| `klap tekst gdag weeireld amen` | Print "gdag weeireld" |
| `gedaan` | "Done" - End of the program |

---

## Step 4: Run It!

You have two ways to run your program:

### Option A: Magic Mode

```bash
python hallo.plats
```

### Option B: CLI Command

```bash
plats run hallo.plats
```

**Output:**

```
gdag weeireld
```

🎉 **Congratulations!** You've written and run your first Platskript program!

---

## Step 5: Try the REPL

Start an interactive session to experiment:

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
>>> zet y op da x derbij getal 10 amen
>>> klap da y amen
15
>>> stop
👋 Tot ziens!
```

See [[REPL Guide]] for more on interactive usage.

---

## Step 6: Explore Examples

VlaamsCodex comes with built-in examples:

```bash
# List all examples
plats examples

# View an example's code
plats examples --show hello

# Run an example
plats examples --run hello

# Save an example to your directory
plats examples --save hello
```

See [[Examples Gallery]] for annotated walkthroughs.

---

## Step 7: Use Your Dialect!

Every command has regional dialect aliases. Use whichever feels most natural:

### Run Commands

| Region | Command |
|--------|---------|
| Standard | `plats run hallo.plats` |
| West-Vlaams | `plats voertuut hallo.plats` |
| Antwerps | `plats doet hallo.plats` |
| Limburgs | `plats gaon hallo.plats` |
| Brussels | `plats doeda hallo.plats` |

### REPL Commands

| Region | Command |
|--------|---------|
| Standard | `plats repl` |
| West-Vlaams | `plats proboir` |
| Antwerps | `plats smos` |
| Limburgs | `plats efkes` |
| Brussels | `plats klansen` |

See [[CLI Reference]] for the complete list of 80+ aliases!

---

## Step 8: Create a Project

Scaffold a new Platskript project:

```bash
plats init mijnproject
cd mijnproject
```

This creates:

```
mijnproject/
├── hallo.plats      # Sample program
└── LEESMIJ.md       # Quick start guide
```

Run the sample program:

```bash
plats run hallo.plats
```

---

## Step 9: Set Up Your IDE

Install the VS Code extension for syntax highlighting:

1. Open VS Code
2. Press `Ctrl+Shift+X` (Extensions)
3. Search for "VlaamsCodex"
4. Click **Install**

See [[VS Code Extension]] for full documentation.

---

## What's Next?

Now that you're set up, continue your journey:

| Goal | Page |
|------|------|
| Learn the language step-by-step | [[Language Tutorial]] |
| See complete syntax reference | [[Language Reference]] |
| Explore all CLI commands | [[CLI Reference]] |
| Learn from example programs | [[Examples Gallery]] |
| Transform text to dialects | [[Dialect Guide]] |

---

## Quick Reference Card

### Program Structure

```platskript
# coding: vlaamsplats
plan doe
  <statements>
gedaan
```

### Common Statements

```platskript
zet x op getal 10 amen              # Variable assignment
klap tekst hello amen               # Print
klap da x amen                      # Print variable
roep greet met tekst world amen     # Function call
geeftterug da x amen                # Return
```

### Function Definition

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
