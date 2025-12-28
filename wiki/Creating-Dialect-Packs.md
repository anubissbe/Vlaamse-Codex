# Creating Dialect Packs

> Build your own dialect transformation rules 📦

This guide shows you how to create custom dialect packs for VlaamsCodex. Whether you want to add a missing regional dialect or create something entirely new, this page covers everything you need.

---

## Overview

Dialect packs are JSON files containing transformation rules. They:
- Convert neutral Dutch/Flemish text to dialect
- Support inheritance from parent packs
- Use three rule types: word, regex, particle
- Protect certain terms from transformation

---

## Quick Start

### 1. Create the Pack File

Create a new JSON file in `dialects/packs/`:

```bash
touch dialects/packs/mijn-dialect.json
```

### 2. Add Basic Structure

```json
{
  "id": "mijn-dialect",
  "label": "Mijn Dialect",
  "inherits": ["algemeen-vlaams"],
  "notes": "My custom dialect pack",
  "protected_terms": [],
  "rules": [
    {"type": "replace_word", "from": "goed", "to": "goe"}
  ]
}
```

### 3. Register in Index

Add to `dialects/index.json`:

```json
{
  "id": "mijn-dialect",
  "label": "Mijn Dialect",
  "inherits": ["algemeen-vlaams"],
  "file": "mijn-dialect.json"
}
```

### 4. Validate

```bash
python tools/validate_dialect_packs.py
```

### 5. Test

```python
from vlaamscodex.dialects.transformer import transform

result = transform("Dat is goed", "mijn-dialect")
print(result)  # "Dat is goe"
```

---

## Pack Structure

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (matches filename without `.json`) |
| `label` | string | Human-readable name |
| `protected_terms` | array | Terms that must not be transformed |
| `rules` | array | Ordered transformation rules |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `inherits` | array | `[]` | Parent pack IDs |
| `notes` | string | `""` | Developer notes (ignored by transformer) |

### Complete Example

```json
{
  "id": "kempisch",
  "label": "Kempisch",
  "inherits": ["antwerps"],
  "notes": "Kempen region dialect features",
  "protected_terms": ["moet", "mag", "zal"],
  "rules": [
    {
      "type": "replace_word",
      "from": "gij",
      "to": "gae",
      "preserve_case": true
    },
    {
      "type": "replace_word",
      "from": "niet",
      "to": "neet"
    },
    {
      "type": "replace_regex",
      "pattern": "\\bdat is\\b",
      "to": "da's",
      "flags": ["IGNORECASE"]
    },
    {
      "type": "append_particle",
      "particle": "jong",
      "probability": 0.15,
      "positions": ["end_of_sentence"]
    }
  ]
}
```

---

## Rule Types

### `replace_word`

Simple whole-word replacement.

```json
{
  "type": "replace_word",
  "from": "goed",
  "to": "goe",
  "case_sensitive": false,
  "preserve_case": true,
  "only_in_questions": false
}
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `from` | string | (required) | Word to match |
| `to` | string | (required) | Replacement text |
| `case_sensitive` | bool | `false` | Match case exactly |
| `preserve_case` | bool | `true` | Keep original word's case |
| `only_in_questions` | bool | `false` | Only apply in `?` sentences |

**Examples:**

```json
// Basic replacement
{"type": "replace_word", "from": "niet", "to": "nie"}

// Case preservation: "Goed" → "Goe", "goed" → "goe"
{"type": "replace_word", "from": "goed", "to": "goe", "preserve_case": true}

// Only in questions: "Waar is dat?" but not "Dat is daar."
{"type": "replace_word", "from": "dat", "to": "da", "only_in_questions": true}
```

---

### `replace_regex`

Regex-based pattern replacement.

```json
{
  "type": "replace_regex",
  "pattern": "\\bdat is\\b",
  "to": "da's",
  "flags": ["IGNORECASE"],
  "preserve_case": false
}
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `pattern` | string | (required) | Python regex pattern |
| `to` | string | (required) | Replacement (supports `\1` backrefs) |
| `flags` | array | `[]` | `IGNORECASE`, `MULTILINE` |
| `preserve_case` | bool | `false` | Preserve matched text case |

**Examples:**

```json
// Contraction
{"type": "replace_regex", "pattern": "\\bdat is\\b", "to": "da's", "flags": ["IGNORECASE"]}

// Pattern with word boundary
{"type": "replace_regex", "pattern": "\\bsch(\\w+)", "to": "sk\\1"}

// Optional letter handling
{"type": "replace_regex", "pattern": "\\b(n?)iet\\b", "to": "\\1ie"}
```

**Important:** Always use `\\b` for word boundaries and escape backslashes in JSON.

---

### `append_particle`

Add discourse particles to sentences.

```json
{
  "type": "append_particle",
  "particle": "zeg",
  "probability": 0.08,
  "positions": ["end_of_sentence"]
}
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `particle` | string | (required) | Text to append |
| `probability` | float | (required) | 0.0-1.0 chance of applying |
| `positions` | array | (required) | Where to add (`["end_of_sentence"]`) |

**Notes:**
- Only active when `enable_particles=True` in transform config
- Idempotent: won't double-append
- Deterministic by default (uses hash-based pseudo-random)

**Common particles by region:**

| Region | Particles |
|--------|-----------|
| Antwerps | `zansen`, `manneke`, `alee` |
| West-Vlaams | `zekers`, `jansen`, `peize` |
| Limburgs | `wansen`, `jansen` |
| Brussels | `allez`, `sava`, `voila` |

---

## Inheritance

### How It Works

Packs can inherit from parent packs:

```json
{
  "id": "mechels",
  "inherits": ["antwerps"],
  ...
}
```

**Inheritance behavior:**

1. Rules accumulate (parent first, then child)
2. Protected terms merge (union)
3. Child rules don't override parent rules—they append

### Inheritance Chain

```
algemeen-vlaams
├── antwerps
│   ├── mechels
│   └── kempen-antwerps
├── west-vlaams
│   └── brugs
└── limburgs
    └── genks
```

### Choosing a Parent

| Parent | Use When |
|--------|----------|
| `algemeen-vlaams` | Starting fresh with common Flemish |
| `antwerps` | Building Antwerp-region variant |
| `west-vlaams` | Building West Flanders variant |
| `limburgs` | Building Limburg variant |
| None | Creating completely independent pack |

---

## Protected Terms

Protected terms are **never** transformed to preserve meaning.

### Global Protected Terms

These are always protected (hardcoded):
- Legal: `verplicht`, `verboden`
- Modal: `moet`, `mag`, `kan`, `zal`
- Conditional: `tenzij`, `behalve`, `alleen`, `enkel`
- Consequence: `boete`, `straf`, `uitzondering`

### Pack-Specific Terms

Add terms specific to your dialect:

```json
{
  "protected_terms": ["specifiek", "jansen", "andere-term"]
}
```

### When to Protect Terms

Protect terms that:
- Have legal or regulatory significance
- Would change meaning if transformed
- Are proper nouns specific to your dialect
- Are technical terms that shouldn't change

---

## Replacement Variables

Use variables in replacement text:

```json
{
  "type": "replace_word",
  "from": "jij",
  "to": "{pronoun_subject}"
}
```

**Built-in variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `{pronoun_subject}` | `ge` | Subject pronoun |
| `{pronoun_object}` | `u` | Object pronoun |
| `{pronoun_possessive}` | `uw` | Possessive pronoun |

Variables are configurable at runtime:

```python
transform(text, "dialect", pronoun_subject="gij")
```

---

## Validation

### Run Validator

```bash
python tools/validate_dialect_packs.py
```

### Checks Performed

| Check | Description |
|-------|-------------|
| JSON syntax | Valid JSON format |
| Required fields | `id`, `label`, `protected_terms`, `rules` present |
| ID format | Matches filename convention |
| Inheritance | Referenced parents exist |
| Cycles | No circular inheritance |
| Rule format | Each rule has required fields |

### Common Errors

| Error | Fix |
|-------|-----|
| `Invalid JSON` | Check commas, quotes, braces |
| `Missing required field` | Add required field |
| `Parent not found` | Check inheritance ID spelling |
| `Circular dependency` | Remove inheritance cycle |

---

## Testing Your Pack

### Python API

```python
from vlaamscodex.dialects.transformer import transform

# Test cases
tests = [
    ("Dat is goed", "Da is goe"),
    ("Gij hebt dat", "Gae hebt da"),
    ("Hoe gaat het?", "Hoe gaat het?"),  # Protected
]

for input_text, expected in tests:
    result = transform(input_text, "mijn-dialect")
    status = "✓" if result == expected else "✗"
    print(f"{status} '{input_text}' → '{result}' (expected: '{expected}')")
```

### CLI

```bash
plats vraag "Dat is goed" --dialect mijn-dialect
```

### Interactive Testing

```python
from vlaamscodex.dialects.transformer import transform

# Interactive testing loop
while True:
    text = input("Enter text (or 'quit'): ")
    if text == 'quit':
        break
    result = transform(text, "mijn-dialect")
    print(f"  → {result}")
```

---

## Best Practices

### Rule Ordering

1. Put most specific rules first
2. Put general patterns after specific words
3. Put particles last

```json
{
  "rules": [
    // 1. Specific word replacements
    {"type": "replace_word", "from": "gijle", "to": "gulder"},
    {"type": "replace_word", "from": "gij", "to": "ge"},

    // 2. General patterns
    {"type": "replace_regex", "pattern": "\\bsch(\\w+)", "to": "sk\\1"},

    // 3. Particles (last)
    {"type": "append_particle", "particle": "zeg", "probability": 0.1, "positions": ["end_of_sentence"]}
  ]
}
```

### Avoid Conflicts

- Don't have overlapping patterns
- Test edge cases
- Consider multi-pass behavior

### Preserve Meaning

- Add terms to `protected_terms` when in doubt
- Test that legal/modal words aren't transformed
- Verify questions still make sense

---

## Pack Generator Tool

Use the generator for scaffolding:

```bash
python tools/generate_dialect_packs.py
```

This creates a starter pack and updates the index.

---

## Example Packs

### Minimal Pack

```json
{
  "id": "minimal",
  "label": "Minimal Example",
  "protected_terms": [],
  "rules": [
    {"type": "replace_word", "from": "goed", "to": "goe"}
  ]
}
```

### Regional Pack

```json
{
  "id": "kust-vlaams",
  "label": "West-Vlaamse Kust",
  "inherits": ["west-vlaams"],
  "notes": "Coastal dialect features",
  "protected_terms": ["vissers", "zee"],
  "rules": [
    {"type": "replace_word", "from": "strand", "to": "stroand"},
    {"type": "replace_word", "from": "water", "to": "woater"},
    {"type": "replace_regex", "pattern": "\\bmeer\\b", "to": "meir"},
    {"type": "append_particle", "particle": "zekers", "probability": 0.2, "positions": ["end_of_sentence"]}
  ]
}
```

### Complete Feature Pack

```json
{
  "id": "feature-complete",
  "label": "Feature Complete Example",
  "inherits": ["algemeen-vlaams"],
  "notes": "Demonstrates all features",
  "protected_terms": ["verplicht", "verboden", "boete"],
  "rules": [
    {
      "type": "replace_word",
      "from": "gij",
      "to": "{pronoun_subject}",
      "preserve_case": true
    },
    {
      "type": "replace_word",
      "from": "niet",
      "to": "nie",
      "case_sensitive": false
    },
    {
      "type": "replace_word",
      "from": "dat",
      "to": "da",
      "only_in_questions": true
    },
    {
      "type": "replace_regex",
      "pattern": "\\bdat is\\b",
      "to": "da's",
      "flags": ["IGNORECASE"]
    },
    {
      "type": "append_particle",
      "particle": "zeg",
      "probability": 0.15,
      "positions": ["end_of_sentence"]
    }
  ]
}
```

---

## Contributing Your Pack

Want to share your dialect pack?

1. Create and test your pack
2. Run validation
3. Fork the repository
4. Add your pack to `dialects/packs/`
5. Update `dialects/index.json`
6. Submit a pull request

**See:** [[Contributing]] for contribution guidelines.

---

## See Also

- [[Dialect-Guide]] - User documentation
- [[Dialect-Engine]] - Technical internals
- [[API-Reference]] - Python API
- [[Contributing]] - Contribution guidelines

---

**Veel plansen!** 🧇
