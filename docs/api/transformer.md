# transformer.py - Dialect Transformation Engine

> `src/vlaamscodex/dialects/transformer.py`

Rule-based text transformation engine that converts standard Dutch/Flemish text to regional dialect variants.

## Overview

The transformer applies dialect-specific rules (word replacements, regex patterns, particles) from JSON dialect packs. It supports inheritance chains, protected terms, and deterministic/non-deterministic modes.

## Main Functions

### `transform(text, dialect_id, **kwargs) -> str`

Transform text using a dialect pack.

**Parameters:**
- `text` (str): Input text to transform
- `dialect_id` (str): Dialect pack ID (e.g., `"west-vlaams/kust"`)
- `deterministic` (bool, optional): Use deterministic randomness (default: True)
- `seed` (int, optional): Seed for deterministic mode (default: 0)
- `enable_particles` (bool, optional): Add dialect particles (default: False)
- `pronoun_subject` (str, optional): Subject pronoun (default: "ge")
- `pronoun_object` (str, optional): Object pronoun (default: "u")
- `pronoun_possessive` (str, optional): Possessive pronoun (default: "uw")
- `max_passes` (int, optional): Maximum transformation passes (default: 3)
- `strict_idempotency` (bool, optional): Raise on non-convergence (default: False)

**Returns:**
- `str`: Transformed text

**Example:**
```python
from vlaamscodex.dialects.transformer import transform

text = "Gij moet dat niet doen."
result = transform(text, "antwerps/stad")
# Result varies by dialect rules
```

---

### `available_packs() -> list[PackInfo]`

List all available dialect packs.

**Returns:**
- `list[PackInfo]`: Sorted list of pack metadata

**Example:**
```python
from vlaamscodex.dialects.transformer import available_packs

for pack in available_packs():
    print(f"{pack.id}: {pack.label}")
    if pack.inherits:
        print(f"  inherits: {', '.join(pack.inherits)}")
```

---

## Data Classes

### `PackInfo`

Metadata about a dialect pack.

```python
@dataclass(frozen=True, slots=True)
class PackInfo:
    id: str           # e.g., "west-vlaams/kust"
    label: str        # e.g., "West-Vlaamse Kust"
    inherits: tuple[str, ...]  # Parent pack IDs
```

### `DialectTransformConfig`

Configuration for transformation behavior.

```python
@dataclass(frozen=True, slots=True)
class DialectTransformConfig:
    deterministic: bool = True
    seed: int = 0
    enable_particles: bool = False
    pronoun_subject: str = "ge"
    pronoun_object: str = "u"
    pronoun_possessive: str = "uw"
    max_passes: int = 3
    strict_idempotency: bool = False
```

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `VLAAMSCODEX_DIALECTS_DIR` | (auto-detect) | Path to dialects directory |
| `VLAAMSCODEX_DIALECT_DETERMINISTIC` | `True` | Deterministic mode |
| `VLAAMSCODEX_DIALECT_SEED` | `0` | Random seed |
| `VLAAMSCODEX_DIALECT_PARTICLES` | `False` | Enable particles |
| `VLAAMSCODEX_PRONOUN_SUBJECT` | `ge` | Subject pronoun |
| `VLAAMSCODEX_PRONOUN_OBJECT` | `u` | Object pronoun |
| `VLAAMSCODEX_PRONOUN_POSSESSIVE` | `uw` | Possessive pronoun |
| `VLAAMSCODEX_DIALECT_MAX_PASSES` | `3` | Max transformation passes |
| `VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY` | `False` | Raise on non-convergence |

---

## Rule Types

### `replace_word`

Simple word replacement with case handling.

```json
{
  "type": "replace_word",
  "from": "gij",
  "to": "ge",
  "preserve_case": true,
  "only_in_questions": false
}
```

### `replace_regex`

Regex-based pattern replacement.

```json
{
  "type": "replace_regex",
  "pattern": "\\bdat\\b",
  "to": "da",
  "flags": ["IGNORECASE"],
  "preserve_case": true
}
```

### `append_particle`

Add dialect particles to sentences.

```json
{
  "type": "append_particle",
  "particle": "zansen",
  "probability": 0.3,
  "positions": ["end_of_sentence"]
}
```

---

## Protected Terms

Certain words are never transformed to preserve meaning:

**Global (always protected):**
- Legal modality: `verplicht`, `verboden`, `mag`, `moet`, `kan`
- Conditions: `tenzij`, `enkel`, `alleen`, `behalve`
- Consequences: `boete`, `straf`, `uitzondering`

**Pack-specific:** Defined in each dialect pack's `protected_terms` array.

---

## Inheritance

Packs can inherit rules from parent packs:

```
antwerps/stad
  └── inherits: antwerps
        └── inherits: algemeen-vlaams
```

Rules are applied in order from most general to most specific.

---

## See Also

- [Dialect Packs Schema](../../dialects/schema.md)
- [Architecture: Dialect Transformer](../architecture/02_dialect_transformer.md)
