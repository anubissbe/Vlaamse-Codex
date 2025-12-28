# CLI Reference

> Complete reference for the `plats` command-line interface 🛠️

VlaamsCodex provides a powerful CLI with **80+ command aliases** from 7 Flemish dialect regions. Use whichever feels most natural!

---

## Overview

```bash
plats <command> [options] [arguments]
```

### All Commands

| Command | Description | Quick Example |
|---------|-------------|---------------|
| `run` | Execute a Platskript file | `plats run script.plats` |
| `build` | Compile to Python file | `plats build script.plats -o out.py` |
| `show-python` | Display generated Python | `plats show-python script.plats` |
| `repl` | Interactive session | `plats repl` |
| `check` | Validate syntax | `plats check script.plats` |
| `examples` | Browse example programs | `plats examples --run hello` |
| `init` | Create new project | `plats init myproject` |
| `fortune` | Random Flemish proverb | `plats fortune` |
| `vraag` | Transform text to dialect | `plats vraag "text" -d antwerps` |
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

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `run`, `loop` | - |
| West-Vlaams | `voertuut` | voer 't uit |
| Oost-Vlaams | `doeme`, `komaan` | doe me, kom aan |
| Antwerps | `doet`, `doeda` | doe 't, doe da |
| Limburgs | `gaon` | gaan |
| Brussels | `doedansen` | doe da |
| Genks | `jaodoen` | ja, doen |
| Vlaams-Brabants | `startop` | start op |

### Examples

```bash
plats run hello.plats           # Standard
plats voertuut hello.plats      # West-Vlaams
plats doet hello.plats          # Antwerps
plats gaon hello.plats          # Limburgs
```

---

## repl - Interactive Session

Start an interactive Platskript session:

```bash
plats repl
```

### REPL Commands

| Command | Action |
|---------|--------|
| `stop` | Exit the REPL |
| `cls` | Clear screen |
| `hulp` | Show help |

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

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `repl` | - |
| West-Vlaams | `proboir` | proberen |
| Oost-Vlaams | `probeer`, `probeertme` | probeer het |
| Antwerps | `smos`, `smossen` | praten/uitproberen |
| Limburgs | `efkes`, `efkesprobieren` | eventjes |
| Brussels | `klansen`, `zwansen` | praten |
| Genks | `probeirme` | probeer het |
| Vlaams-Brabants | `probeerdansen` | probeer da |

See [[REPL Guide]] for detailed usage.

---

## check - Validate Syntax

Check a file for syntax errors without running it:

```bash
plats check script.plats
```

### Dialect-Specific Error Messages

Errors come in your dialect when using dialect aliases:

```bash
# West-Vlaams
$ plats zijdezekers script.plats
# Error: Jansen, ge zijt 'amen' vergeten op lijn 5!

# Antwerps
$ plats istdagoe script.plats
# Error: Manneke, gij zijt 'amen' vergeten op lijn 5!

# Limburgs
$ plats kloptda script.plats
# Error: Jansen, gae zeet 'amen' vergeate op lien 5!
```

### Multi-Vlaams Aliases

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `check` | - |
| West-Vlaams | `zijdezekers`, `zekers`, `okeej` | zijt ge zeker? |
| Oost-Vlaams | `zalkdagaan`, `checktem` | zal da gaan? |
| Antwerps | `istdagoe`, `isdatgoe`, `goeddansen` | is da goe? |
| Limburgs | `kloptda`, `kloptdat`, `goedzowie` | klopt da? |
| Brussels | `passedat`, `camarche` | passe da? |
| Genks | `jaowklopt`, `probeircheck` | ja, klopt |
| Vlaams-Brabants | `checkdansen` | check da |

---

## build - Compile to Python

Convert Platskript to Python source file:

```bash
plats build script.plats --out output.py
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--out`, `-o` | Output file path | `<name>.py` |

### Multi-Vlaams Aliases

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `build`, `bouw` | - |
| West-Vlaams | `moakt` | maakt |
| Oost-Vlaams | `moaktme` | maak het |
| Antwerps | `bouwt` | bouwt |
| Limburgs | `maakt` | maakt |
| Brussels | `bouwtda` | bouw da |
| Genks | `maktme` | maak het |
| Vlaams-Brabants | `maakda` | maak da |

---

## show-python - View Generated Code

Display the transpiled Python without saving:

```bash
plats show-python script.plats
```

### Example Output

```bash
$ plats show-python hello.plats
# Transpiled from hello.plats
naam = 'weeireld'
def groet(wie):
    print('gdag' + ' ' + 'aan' + ' ' + wie)
groet(naam)
```

### Multi-Vlaams Aliases

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `show-python`, `toon` | - |
| West-Vlaams | `tuunt`, `tuuntnekeer` | toon eens |
| Oost-Vlaams | `toontme` | toon het |
| Antwerps | `toont`, `toondada` | toon da da |
| Limburgs | `loatziejn`, `loatskiejn` | laat zien |
| Brussels | `toonmansen` | toon ze |
| Genks | `loatkieke` | laat kijken |
| Vlaams-Brabants | `loatkiejke` | laat kijken |

---

## examples - Browse Examples

List and run built-in example programs:

```bash
# List all examples
plats examples

# Show example source code
plats examples --show hello

# Run an example
plats examples --run hello

# Save example to current directory
plats examples --save hello
```

### Available Examples

| Name | Description |
|------|-------------|
| `hello` | Hello World with function |
| `funksies` | Function definitions and calls |
| `teller` | Counter with loop |
| `begroeting` | Greeting with string concatenation |
| `rekenmachine` | Arithmetic operations |

### Options

| Option | Description |
|--------|-------------|
| `--show NAME` | Display example source code |
| `--run NAME` | Execute the example |
| `--save NAME` | Save to `NAME.plats` |

### Multi-Vlaams Aliases

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `examples` | - |
| West-Vlaams | `tuuntnekeer`, `voorbeeldskes`, `tuuntse` | toon eens, voorbeeldjes |
| Oost-Vlaams | `ziedievoorbeelden`, `toontdie` | zie die voorbeelden |
| Antwerps | `toondada`, `voorbeeldekes` | toon da da |
| Limburgs | `loatskiejn`, `voorbeeldjes`, `kiekenseffe` | laat kijken |
| Brussels | `toontmansen`, `voorbeeldansen` | toon ze |
| Genks | `jaowkiek` | ja, kijk |
| Vlaams-Brabants | `voorbeeldanse` | voorbeelden |

See [[Examples Gallery]] for detailed walkthroughs.

---

## init - Create Project

Scaffold a new Platskript project:

```bash
plats init myproject
```

### Created Files

```
myproject/
├── hallo.plats      # Sample program
└── LEESMIJ.md       # Quick start guide (Flemish README)
```

### Multi-Vlaams Aliases

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `init` | - |
| West-Vlaams | `allehop`, `startop`, `beginme` | hier gaan we! |
| Oost-Vlaams | `komaan`, `komme` | kom aan |
| Antwerps | `awel`, `aweldan` | awel, beginnen |
| Limburgs | `allei`, `gaonme` | vooruit |
| Brussels | `allez`, `allezdan` | allez |
| Genks | `jaowel` | jawel |
| Vlaams-Brabants | `startdansen` | start da |

---

## fortune - Random Proverb

Display a random Flemish proverb or wisdom:

```bash
plats fortune
```

### Example Output

```
╔════════════════════════════════════════╗
║ Beter een vogel in de hand dan tien    ║
║ op 't dak, jong!                       ║
╚════════════════════════════════════════╝
```

### Multi-Vlaams Aliases

| Region | Aliases | Meaning |
|--------|---------|---------|
| Standard | `fortune` | - |
| West-Vlaams | `zegt`, `zenmoederzegt`, `spreuke` | zen moeder zegt |
| Oost-Vlaams | `spreuk`, `gezegd` | spreuk |
| Antwerps | `watteda`, `manneke` | wat is da? |
| Limburgs | `wiste`, `wistedak` | wist ge dat? |
| Brussels | `zansen`, `eikes` | zwanzen |
| Genks | `jaow` | ja |
| Vlaams-Brabants | `zegansen` | zeg |

---

## vraag - Transform Text

Transform standard Dutch/Flemish text into regional dialect:

```bash
plats vraag "Gij moet dat doen." --dialect antwerps
```

### Options

| Option | Description |
|--------|-------------|
| `--dialect`, `-d` | Target dialect ID (required) |
| `--particles` | Enable dialect particle insertion |
| `--seed` | Random seed for reproducibility |

### Examples

```bash
# Transform to Antwerps
$ plats vraag "Gij hebt dat goed gedaan" --dialect antwerps
Ge hebt da goe gedaan

# Transform to West-Vlaams
$ plats vraag "Gij hebt dat goed gedaan" --dialect west-vlaams
Gie ej da goed gedoan

# With particles
$ plats vraag "Dat is goed" --dialect antwerps --particles
Da's goe, zansen
```

See [[Dialect Guide]] for comprehensive dialect documentation.

---

## dialecten - List Dialects

Show all available dialect packs:

```bash
plats dialecten
```

### Output

```
Available dialect packs (84 total):

algemeen-vlaams (7 regions)
├── antwerps/        - Antwerpen area (12 packs)
├── brussels/        - Brussels area (12 packs)
├── limburgs/        - Limburg area (12 packs)
├── oost-vlaams/     - Oost-Vlaanderen (12 packs)
├── vlaams-brabants/ - Vlaams-Brabant (12 packs)
├── west-vlaams/     - West-Vlaanderen (12 packs)
└── genks/           - Genk area (5 packs)
```

---

## help - Show Help

Display help information:

```bash
plats help           # English
plats haalp          # Flemish variant
```

### Multi-Vlaams Aliases

| Region | Aliases |
|--------|---------|
| Standard | `help`, `haalp` |
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

| Region | Aliases |
|--------|---------|
| Standard | `version`, `versie` |
| West-Vlaams | `welke` |
| Brussels | `welkansen` |
| Genks | `versje` |

---

## Magic Mode

Run `.plats` files directly with Python:

```bash
python script.plats
```

### Requirements

File must have the encoding header:

```platskript
# coding: vlaamsplats
plan doe
  ...
gedaan
```

### How It Works

1. Python reads `# coding: vlaamsplats` (PEP 263)
2. VlaamsCodex registers the `vlaamsplats` codec at startup
3. The codec transpiles Platskript → Python
4. Python executes the generated code

### Limitations

| Flag | Issue |
|------|-------|
| `python -S` | Disables site module, codec not registered |
| `python -I` | Isolated mode, codec not registered |

**Fallback:** Use `plats run script.plats`

See [[Magic Mode]] for technical details.

---

## Dialect Regions Summary

VlaamsCodex supports 7 major Flemish dialect regions:

| Region | Character | Example Greeting |
|--------|-----------|------------------|
| **West-Vlaams** | Coastal, rugged | "Ojansen!" |
| **Oost-Vlaams** | Eastern variants | "Eej!" |
| **Antwerps** | Urban, energetic | "Alee manneke!" |
| **Limburgs** | Melodic, soft | "Houdoe!" |
| **Brussels** | Mixed, playful | "Allez, sava?" |
| **Genks** | Mining heritage | "Jaow!" |
| **Vlaams-Brabants** | Central region | "Wa zegde?" |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VLAAMSCODEX_DIALECTS_DIR` | auto | Override dialect packs location |
| `VLAAMSCODEX_DIALECT_DETERMINISTIC` | `True` | Reproducible transformations |
| `VLAAMSCODEX_DIALECT_SEED` | `0` | Random seed |
| `VLAAMSCODEX_DIALECT_PARTICLES` | `False` | Enable particles |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Syntax error in Platskript |
| 3 | File not found |

---

## See Also

- [[Getting Started]] - Installation and first steps
- [[REPL Guide]] - Interactive session details
- [[Dialect Guide]] - Text transformation system
- [[Examples Gallery]] - Sample programs

---

**'t Es simpel, 't es plansen!** 🧇
