# Dialect Guide

> Transform text into 84 Flemish regional dialects! 🇧🇪

VlaamsCodex includes a powerful dialect transformation engine that converts standard Dutch/Flemish text into regional dialect variations. Educational, entertaining, and authentically Flemish!

---

## Quick Start

### Command Line

```bash
# Transform text to Antwerps
plats vraag "Gij hebt dat goed gedaan" --dialect antwerps
# Output: Ge hebt da goe gedaan

# List available dialects
plats dialecten
```

### Python API

```python
from vlaamscodex.dialects.transformer import transform, available_packs

# Transform text
result = transform("Gij hebt dat goed gedaan", "antwerps")
print(result)  # Ge hebt da goe gedaan

# List available packs
for pack in available_packs():
    print(f"{pack.name}: {pack.description}")
```

---

## Available Dialects

VlaamsCodex includes **84 dialect packs** across 7 major regions:

### Dialect Regions

| Region | Pack Count | Character |
|--------|------------|-----------|
| **Algemeen Vlaams** | 7 | Base/standard Flemish |
| **West-Vlaams** | 12 | Coastal, rugged, distinctive |
| **Oost-Vlaams** | 12 | Eastern variants |
| **Antwerps** | 12 | Urban, energetic |
| **Limburgs** | 12 | Melodic, soft tones |
| **Brussels** | 12 | Mixed French influence |
| **Vlaams-Brabants** | 12 | Central region |
| **Genks** | 5 | Mining heritage |

### Example Packs by Region

**West-Vlaams:**
- `west-vlaams` (base)
- `brugs` (Bruges)
- `kortrijks` (Kortrijk)
- `roeselaars` (Roeselare)
- `iepersk` (Ieper)

**Antwerps:**
- `antwerps` (base)
- `mechels` (Mechelen)
- `kempen-antwerps` (Kempen)
- `lansen` (Lier area)

**Limburgs:**
- `limburgs` (base)
- `hasselts` (Hasselt)
- `genks` (Genk)
- `maaseiks` (Maaseik)

### List All Dialects

```bash
plats dialecten
```

---

## Transformation Rules

Each dialect pack contains rules that transform text:

### Word Replacements

Simple word-to-word mappings:

| Standard | Antwerps | West-Vlaams | Limburgs |
|----------|----------|-------------|----------|
| gij | ge | gie | gae |
| niet | nie | ni | neet |
| dat | da | da | det |
| goed | goe | goed | good |
| hebben | emmen | en | höbbe |

### Pattern Rules

Regular expression transformations:

| Pattern | Result | Example | Dialect |
|---------|--------|---------|---------|
| `ij` → `è` | `wijn` → `wèn` | Brussels |
| `ui` → `uu` | `huis` → `huus` | Limburgs |
| `sch` → `sk` | `school` → `skool` | West-Vlaams |
| `oo` → `ao` | `groot` → `graot` | West-Vlaams |

### Particles

Optional dialect particles add authenticity:

| Dialect | Particles |
|---------|-----------|
| Antwerps | `zansen`, `manneke`, `alee` |
| West-Vlaams | `zekers`, `jansen`, `peize` |
| Limburgs | `wansen`, `jansen` |
| Brussels | `allez`, `sava`, `voila` |

Enable with `--particles`:

```bash
plats vraag "Dat is goed" --dialect antwerps --particles
# Output: Da's goe, zansen
```

---

## Command Line Usage

### Basic Transform

```bash
plats vraag "<text>" --dialect <dialect-id>
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--dialect` | `-d` | Target dialect (required) |
| `--particles` | | Enable particle insertion |
| `--seed` | | Random seed for reproducibility |

### Examples

```bash
# Transform to different dialects
plats vraag "Gij hebt dat goed gedaan" --dialect antwerps
# Ge hebt da goe gedaan

plats vraag "Gij hebt dat goed gedaan" --dialect west-vlaams
# Gie ej da goed gedoan

plats vraag "Gij hebt dat goed gedaan" --dialect limburgs
# Gae höb det good gedoan

plats vraag "Gij hebt dat goed gedaan" --dialect brussels
# Gij eit da goe gedoan
```

---

## Python API

### Basic Transform

```python
from vlaamscodex.dialects.transformer import transform

text = "Gij hebt dat goed gedaan"
result = transform(text, "antwerps")
print(result)  # Ge hebt da goe gedaan
```

### With Configuration

```python
from vlaamscodex.dialects.transformer import transform, DialectTransformConfig

config = DialectTransformConfig(
    deterministic=True,      # Reproducible output
    seed=42,                 # Random seed
    enable_particles=True,   # Add dialect particles
    max_passes=5            # Transformation iterations
)

result = transform("Dat is goed", "antwerps", config=config)
print(result)  # Da's goe, zansen
```

### List Available Packs

```python
from vlaamscodex.dialects.transformer import available_packs

for pack in available_packs():
    print(f"{pack.name}")
    print(f"  Region: {pack.region}")
    print(f"  Rules: {pack.rule_count}")
    print(f"  Inherits: {pack.inherits_from}")
```

### PackInfo Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Pack identifier |
| `region` | str | Geographic region |
| `description` | str | Human-readable description |
| `rule_count` | int | Number of transformation rules |
| `inherits_from` | str | Parent pack name |

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VLAAMSCODEX_DIALECT_DETERMINISTIC` | `true` | Reproducible output |
| `VLAAMSCODEX_DIALECT_SEED` | `0` | Random seed |
| `VLAAMSCODEX_DIALECT_PARTICLES` | `false` | Enable particles |
| `VLAAMSCODEX_DIALECT_MAX_PASSES` | `3` | Max iterations |
| `VLAAMSCODEX_DIALECTS_DIR` | auto | Custom dialects directory |

### Pronoun Overrides

Customize pronoun transformations:

| Variable | Default | Description |
|----------|---------|-------------|
| `VLAAMSCODEX_PRONOUN_SUBJECT` | `ge` | Subject pronoun |
| `VLAAMSCODEX_PRONOUN_OBJECT` | `u` | Object pronoun |
| `VLAAMSCODEX_PRONOUN_POSSESSIVE` | `uw` | Possessive pronoun |

---

## Dialect Pack Structure

Each pack is a JSON file:

```json
{
  "metadata": {
    "name": "antwerps",
    "region": "Antwerpen",
    "description": "Antwerps dialect",
    "inherits": "algemeen-vlaams"
  },
  "rules": {
    "words": {
      "gij": "ge",
      "niet": "nie",
      "dat": "da"
    },
    "patterns": [
      {
        "pattern": "\\bgoed\\b",
        "replacement": "goe",
        "probability": 1.0
      }
    ],
    "particles": ["zansen", "manneke"]
  },
  "protected_terms": ["moet", "zal", "kan", "mag"]
}
```

### Rule Types

| Type | Description | Example |
|------|-------------|---------|
| `words` | Simple replacements | `"gij": "ge"` |
| `patterns` | Regex patterns | `"\\bgoed\\b": "goe"` |
| `particles` | End-of-sentence additions | `["zansen", "manneke"]` |

---

## Inheritance Model

Dialect packs can inherit from parents:

```
algemeen-vlaams (base)
├── antwerps
│   ├── mechels
│   └── kempen-antwerps
├── west-vlaams
│   ├── brugs
│   └── kortrijks
└── limburgs
    ├── hasselts
    └── genks
```

Child packs:
- Inherit all parent rules
- Can override specific rules
- Can add new rules
- Protected terms merge

---

## Examples

### Compare Dialects

```python
from vlaamscodex.dialects.transformer import transform

text = "Gij hebt dat goed gedaan vandaag"
dialects = ["antwerps", "west-vlaams", "limburgs", "brussels"]

for dialect in dialects:
    result = transform(text, dialect)
    print(f"{dialect:15} {result}")
```

Output:

```
antwerps        Ge hebt da goe gedaan vandaag
west-vlaams     Gie ej da goed gedoan vandoage
limburgs        Gae höb det good gedoan vandaag
brussels        Gij eit da goe gedoan vandaag
```

### Batch Processing

```python
from vlaamscodex.dialects.transformer import transform

texts = [
    "Hoe gaat het met u?",
    "Dat is een mooie dag.",
    "Waar woont gij?"
]

for text in texts:
    print(f"Original: {text}")
    print(f"Antwerps: {transform(text, 'antwerps')}")
    print()
```

### With Particles

```bash
# Without particles
plats vraag "Dat is heel mooi" --dialect antwerps
# Da is heel mooi

# With particles
plats vraag "Dat is heel mooi" --dialect antwerps --particles
# Da is heel mooi, zansen
```

---

## Protected Terms

Some terms are never transformed to preserve meaning:

### Legal/Modal Terms

Words like `moet`, `zal`, `kan`, `mag` are protected because transforming them could change legal or modal meaning.

### Proper Nouns

Capitalized words (names, places) are typically protected.

### Technical Terms

Domain-specific vocabulary may be protected in specialized packs.

---

## Idempotency

The transformer is idempotent—applying the same transformation twice produces the same result:

```python
text = "Gij hebt dat gedaan"
once = transform(text, "antwerps")
twice = transform(once, "antwerps")
assert once == twice  # True: "Ge hebt da gedaan"
```

This prevents "drift" when text is accidentally re-transformed.

---

## Creating Custom Packs

See [[Creating Dialect Packs]] for a complete guide to:
- Pack JSON structure
- Rule type syntax
- Inheritance setup
- Validation tools
- Testing approaches

---

## See Also

- [[CLI Reference]] - `vraag` and `dialecten` commands
- [[API Reference]] - `transformer` module documentation
- [[Creating Dialect Packs]] - Create your own dialect
- [[Dialect Engine]] - Technical internals

---

**Veel plansen!** 🧇
