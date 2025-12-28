# Dialect Transformation Guide

> Transform Dutch/Flemish text into regional dialect variants.

## What is Dialect Transformation?

VlaamsCodex includes a powerful text transformation engine that converts standard Dutch or Flemish text into authentic regional dialect variants. This is perfect for:

- Adding local flavor to applications
- Learning about Flemish dialects
- Creating dialect-aware content
- Having fun with language!

---

## Quick Start

### Transform Text

```bash
plats vraag "Gij moet dat doen." --dialect antwerps
```

**Output:** A transformed version with Antwerp dialect features.

### List Available Dialects

```bash
plats dialecten
```

---

## Available Dialect Packs

VlaamsCodex includes **80+ dialect packs** covering all Flemish regions:

### Main Regions

| Region | Pack ID | Description |
|--------|---------|-------------|
| General | `algemeen-vlaams` | Base Flemish transformations |
| Antwerp | `antwerps` | Antwerp city dialect |
| West Flanders | `west-vlaams` | West Flemish dialect |
| East Flanders | `oost-vlaams` | East Flemish dialect |
| Limburg | `limburgs` | Limburgish dialect |
| Flemish Brabant | `vlaams-brabants` | Brabantian dialect |
| Brussels | `brussels` | Brussels Flemish |

### Sub-Dialects

Each region has specialized sub-dialects:

**Antwerp:**
- `antwerps/haven` - Harbor workers' dialect
- `antwerps/stad` - City center
- `antwerps/kempisch` - Campine region

**West Flanders:**
- `west-vlaams/kust` - Coastal dialect
- `west-vlaams/brugge` - Bruges area
- `west-vlaams/kortrijk` - Kortrijk area

**Limburg:**
- `limburgs/genk` - Genk dialect
- `limburgs/hasselt` - Hasselt area
- `limburgs/maasland` - Maasland region

---

## Using the CLI

### Basic Usage

```bash
plats vraag "Het is een mooie dag." --dialect antwerps
```

### Specify Seed for Reproducibility

```bash
plats vraag "Het is mooi weer." --dialect antwerps --seed 42
```

Using the same seed produces identical output, useful for testing.

### List All Packs

```bash
plats dialecten
```

Output:
```
Available dialect packs (83 total):

  algemeen-vlaams           Algemeen Vlaams
  antwerps                  Antwerps
  antwerps/haven            Antwerps (Haven)
  antwerps/kempisch         Antwerps (Kempisch)
  west-vlaams               West-Vlaams
  west-vlaams/kust          West-Vlaams (Kust)
  ...
```

---

## Example Transformations

### Standard to Antwerps

**Input:**
```
Gij moet dat boek lezen.
```

**Output (Antwerps):**
```
Gij mot da boek lezen, zansen.
```

### Standard to West-Vlaams

**Input:**
```
Het is vandaag mooi weer.
```

**Output (West-Vlaams):**
```
't Is vandoage schoon weer, jansen.
```

### Standard to Limburgs

**Input:**
```
Dat is een goed idee.
```

**Output (Limburgs):**
```
Da is 'n good idee, wansen.
```

---

## Transformation Features

### Word Replacements

Common transformations:

| Standard | Antwerps | West-Vlaams | Limburgs |
|----------|----------|-------------|----------|
| dat | da | da | da |
| gij | ge | gie | gij |
| niet | nie | nie | neet |
| mooi | schoon | schoon | sjoon |
| goed | goe | goe | good |

### Particles

Dialects add characteristic particles:

| Dialect | Particles | Usage |
|---------|-----------|-------|
| Antwerps | zansen, manneke | End of sentences |
| West-Vlaams | jansen, zekers | Emphasis |
| Limburgs | wansen, zjwansen | End of sentences |
| Brussels | allez, hein | Interjections |

### Pronunciation Patterns

| Pattern | Example | Result |
|---------|---------|--------|
| `ij` → `aa` | "wij" | "waa" |
| `ui` → `uu` | "huis" | "huus" |
| dropping final `t` | "dat" | "da" |

---

## Protected Terms

Certain words are **never transformed** to preserve meaning:

| Category | Examples |
|----------|----------|
| Legal | verplicht, verboden, boete, straf |
| Modality | moet, kan, mag, niet |
| Exceptions | tenzij, behalve, uitzondering |

This ensures legal or official text maintains its precision.

---

## Inheritance System

Dialect packs can inherit from parent packs:

```
algemeen-vlaams
├── antwerps
│   ├── antwerps/haven
│   ├── antwerps/stad
│   └── antwerps/kempisch
├── west-vlaams
│   ├── west-vlaams/kust
│   └── west-vlaams/brugge
└── limburgs
    ├── limburgs/genk
    └── limburgs/hasselt
```

Child packs apply parent rules first, then add their own specializations.

---

## CLI Commands by Dialect

All CLI commands have dialect-specific aliases:

### Run Commands

| Dialect | Alias | Standard |
|---------|-------|----------|
| West-Vlaams | `voertuut` | `run` |
| Antwerps | `doet` | `run` |
| Limburgs | `gaon` | `run` |
| Brussels | `doeda` | `run` |

### REPL Commands

| Dialect | Alias | Standard |
|---------|-------|----------|
| West-Vlaams | `proboir` | `repl` |
| Antwerps | `smos` | `repl` |
| Limburgs | `efkes` | `repl` |
| Brussels | `klansen` | `repl` |

### Error Messages

When using dialect aliases, error messages come in that dialect:

```bash
# Using Antwerps checker
plats istdagoe script.plats
# Manneke, gij zijt 'amen' vergeten op lijn 5!

# Using West-Vlaams checker
plats zijdezekers script.plats
# Jansen, ge zijt 'amen' vergeten op lijn 5!
```

---

## Tips for Best Results

### 1. Start with Clean Text

Input text should be standard Dutch/Flemish without spelling errors.

### 2. Use Appropriate Dialect

Choose a dialect that matches your target audience:
- `antwerps` - Urban, casual
- `west-vlaams` - Coastal, traditional
- `limburgs` - Melodic, soft

### 3. Use Seeds for Consistency

For reproducible results in testing or production:

```bash
plats vraag "tekst" --dialect antwerps --seed 12345
```

### 4. Try Sub-Dialects

For more authentic regional flavor, use specific sub-dialects:

```bash
plats vraag "tekst" --dialect antwerps/haven  # Harbor dialect
plats vraag "tekst" --dialect west-vlaams/kust # Coastal dialect
```

---

## What's Next?

- **[CLI Reference](cli-reference.md)**: All commands in detail
- **[Language Tutorial](language-tutorial.md)**: Learn Platskript
- **[Quick Start](quick-start.md)**: Get running fast

---

**Veel plansen!** 🧇
