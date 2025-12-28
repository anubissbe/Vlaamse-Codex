# CLI Reference

> Complete reference for all VlaamsCodex commands.

## Command Overview

| Command | Description | Example |
|---------|-------------|---------|
| `run` | Execute a Platskript file | `plats run script.plats` |
| `build` | Compile to Python file | `plats build script.plats -o out.py` |
| `show-python` | Display generated Python | `plats show-python script.plats` |
| `repl` | Interactive session | `plats repl` |
| `examples` | Browse example programs | `plats examples --run hello` |
| `check` | Validate syntax | `plats check script.plats` |
| `init` | Create new project | `plats init myproject` |
| `fortune` | Random Flemish proverb | `plats fortune` |
| `vraag` | Transform text to dialect | `plats vraag "text" --dialect antwerps` |
| `dialecten` | List available dialects | `plats dialecten` |
| `help` | Show help | `plats help` |
| `version` | Show version | `plats version` |

---

## run - Execute Programs

Run a Platskript file:

```bash
plats run script.plats
```

### Multi-Vlaams Aliases

| Region | Alias | Example |
|--------|-------|---------|
| Standard | `loop` | `plats loop script.plats` |
| West-Vlaams | `voertuut` | `plats voertuut script.plats` |
| Oost-Vlaams | `doeme` | `plats doeme script.plats` |
| Antwerps | `doet`, `doeda` | `plats doet script.plats` |
| Limburgs | `gaon` | `plats gaon script.plats` |
| Brussels | `doedansen` | `plats doedansen script.plats` |
| Genks | `jaodoen` | `plats jaodoen script.plats` |

---

## build - Compile to Python

Convert Platskript to Python source:

```bash
plats build script.plats --out output.py
```

### Options

| Option | Description |
|--------|-------------|
| `--out`, `-o` | Output file path |

### Multi-Vlaams Aliases

| Region | Alias |
|--------|-------|
| Standard | `bouw` |
| West-Vlaams | `moakt` |
| Oost-Vlaams | `moaktme` |
| Antwerps | `bouwt` |
| Limburgs | `maakt` |
| Brussels | `bouwtda` |
| Genks | `maktme` |

---

## show-python - View Generated Code

Display the Python code without saving:

```bash
plats show-python script.plats
```

Example output:
```python
naam = 'weeireld'
def groet(wie):
    print('gdag' + ' ' + 'aan' + ' ' + wie)
groet(naam)
```

### Multi-Vlaams Aliases

| Region | Alias |
|--------|-------|
| Standard | `toon` |
| West-Vlaams | `tuunt`, `tuuntnekeer` |
| Oost-Vlaams | `toontme` |
| Antwerps | `toont`, `toondada` |
| Limburgs | `loatziejn`, `loatskiejn` |
| Brussels | `toonmansen` |
| Genks | `loatkieke` |

---

## repl - Interactive Session

Start an interactive Platskript session:

```bash
plats repl
```

### REPL Commands

| Command | Description |
|---------|-------------|
| `stop` | Exit the REPL |
| `help` | Show REPL help |

### Example Session

```
🧇 Platskript REPL (type 'stop' om te stoppen)
>>> zet naam op tekst Claude amen
>>> klap tekst hallo plakt spatie plakt da naam amen
hallo Claude
>>> stop
👋 Tot ziens!
```

### Multi-Vlaams Aliases

| Region | Alias | Meaning |
|--------|-------|---------|
| West-Vlaams | `proboir` | proberen |
| Oost-Vlaams | `probeer`, `probeertme` | probeer het |
| Antwerps | `smos`, `smossen` | praten/uitproberen |
| Limburgs | `efkes`, `efkesproberen` | eventjes proberen |
| Brussels | `klansen`, `zwansen` | praten |
| Genks | `probeirme` | probeer het |

---

## examples - Browse Examples

List and run example programs:

```bash
# List all examples
plats examples

# Show example code
plats examples --show hello

# Run an example
plats examples --run hello

# Save example to file
plats examples --save hello
```

### Available Examples

| Name | Description |
|------|-------------|
| `hello` | Hello World with function |
| `funksies` | Function definitions and calls |
| `teller` | Counter with variables |
| `begroeting` | Greeting message |
| `rekenmachine` | Arithmetic operations |

### Options

| Option | Description |
|--------|-------------|
| `--show NAME` | Display the example code |
| `--run NAME` | Execute the example |
| `--save NAME` | Save to `NAME.plats` |

### Multi-Vlaams Aliases

| Region | Alias | Meaning |
|--------|-------|---------|
| West-Vlaams | `tuuntnekeer` | toon eens |
| Oost-Vlaams | `toontme` | toon het mij |
| Antwerps | `toondada` | toon da da |
| Limburgs | `loatskiejn` | laat 's kijken |
| Brussels | `toonmansen` | toon ze |
| Genks | `jaowkiek` | jaow, kijk |

---

## check - Validate Syntax

Check a file for syntax errors:

```bash
plats check script.plats
```

### Dialect Error Messages

Errors come in your dialect:

```bash
# Using West-Vlaams alias
plats zijdezekers script.plats
# Error: Jansen, ge zijt 'amen' vergeten op lijn 5!

# Using Antwerps alias
plats istdagoe script.plats
# Error: Manneke, gij zijt 'amen' vergeten op lijn 5!
```

### Multi-Vlaams Aliases

| Region | Alias | Meaning |
|--------|-------|---------|
| West-Vlaams | `zijdezekers`, `zekers` | zijt ge zeker? |
| Oost-Vlaams | `kontroleer` | controleer |
| Antwerps | `istdagoe`, `isgoe` | is da goe? |
| Limburgs | `kloptda`, `kloptdak` | klopt da? |
| Brussels | `checkda` | check da |
| Genks | `kloptdame` | klopt da me? |

---

## init - Create Project

Create a new Platskript project:

```bash
plats init myproject
```

Creates:
```
myproject/
├── hallo.plats      # Sample program
└── LEESMIJ.md       # Quick start guide
```

### Multi-Vlaams Aliases

| Region | Alias | Meaning |
|--------|-------|---------|
| West-Vlaams | `allehop`, `beginme` | hier gaan we! |
| Oost-Vlaams | `komaan`, `komme` | kom aan |
| Antwerps | `awel`, `aweldan` | kom, we beginnen |
| Limburgs | `allei`, `gaonme` | vooruit dan |
| Brussels | `allez`, `allezdan` | allez |
| Genks | `jaowel` | jaowel |

---

## fortune - Random Proverb

Display a random Flemish proverb:

```bash
plats fortune
# "Beter een vogel in de hand dan tien in de lucht."
```

### Multi-Vlaams Aliases

| Region | Alias | Meaning |
|--------|-------|---------|
| West-Vlaams | `zegt`, `zenmoederzegt`, `spreuke` | zen moeder zegt... |
| Oost-Vlaams | `spreuk`, `gezegd` | spreuk |
| Antwerps | `watteda`, `manneke` | wat is da? |
| Limburgs | `wiste`, `wistedak` | wist ge dat? |
| Brussels | `zansen`, `eikes` | zwanzen |
| Genks | `jaow` | jaow |

---

## vraag - Transform Text

Transform standard Dutch/Flemish to regional dialect:

```bash
plats vraag "Gij moet dat doen." --dialect antwerps
# "Gij mot da doen, zansen."
```

### Options

| Option | Description |
|--------|-------------|
| `--dialect`, `-d` | Target dialect ID |
| `--seed` | Random seed for reproducibility |

### Example

```bash
plats vraag "Het is een mooie dag vandaag." --dialect west-vlaams
```

---

## dialecten - List Dialects

Show all available dialect packs:

```bash
plats dialecten
```

Output:
```
Available dialect packs:
  algemeen-vlaams     Algemeen Vlaams
  antwerps            Antwerps
  antwerps/haven      Antwerps (haven)
  west-vlaams         West-Vlaams
  ...
```

---

## help - Show Help

Display help information:

```bash
plats help          # English
plats haalp         # Flemish
```

### Multi-Vlaams Aliases

| Region | Alias |
|--------|-------|
| Standard | `haalp` |
| West-Vlaams | `hulpe` |
| Oost-Vlaams | `hulpme` |
| Antwerps | `helptemij` |
| Limburgs | `helpt` |
| Brussels | `helpansen` |
| Genks | `helptme` |

---

## version - Show Version

Display version information:

```bash
plats version
# VlaamsCodex v0.2.0
```

### Multi-Vlaams Aliases

| Region | Alias |
|--------|-------|
| Standard | `versie` |
| West-Vlaams | `welke` |
| Brussels | `welkansen` |
| Genks | `versje` |

---

## Magic Mode

Run `.plats` files directly with Python:

```bash
python script.plats
```

**Requirement**: File must have encoding header:

```platskript
# coding: vlaamsplats
plan doe
  ...
gedaan
```

### How It Works

1. Python reads `# coding: vlaamsplats` (PEP 263)
2. VlaamsCodex registers the `vlaamsplats` codec at startup
3. The codec transpiles Platskript to Python
4. Python executes the generated code

### Limitations

- Doesn't work with `python -S` (disables site module)
- Doesn't work with `python -I` (isolated mode)
- Fallback: use `plats run script.plats`

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Syntax error in Platskript |

---

**'t Es simpel, 't es plansen!** 🧇
