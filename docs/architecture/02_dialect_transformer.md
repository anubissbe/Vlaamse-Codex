# Dialect Transformer Architecture

The dialect transformer is a rule-based text transformation system that converts neutral Dutch text into various Flemish dialect styles.

## Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Dialect Transformer                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Input Text ──▶ [Mask Protected] ──▶ [Apply Rules] ──▶ [Unmask] ──▶ Out │
│                         │                   │                            │
│                         ▼                   ▼                            │
│                 ┌───────────────┐   ┌───────────────┐                   │
│                 │ Global +      │   │ Resolved Pack │                   │
│                 │ Pack-specific │   │ (inheritance  │                   │
│                 │ protected     │   │  chain)       │                   │
│                 │ terms         │   └───────────────┘                   │
│                 └───────────────┘                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Transformer Engine (`transformer.py`)

The main entry point is `transform(text, dialect_id, **config)`:

```python
from vlaamscodex.dialects.transformer import transform, available_packs

# List available dialects
packs = available_packs()  # Returns list of PackInfo

# Transform text
result = transform(
    "Dat is goed.",
    "vlaams/antwerps",
    enable_particles=True  # Optional: add discourse particles
)
# Result: "Da's goe, zeg."
```

### 2. Dialect Registry (`_DialectRegistry`)

Manages pack loading and inheritance resolution:

- **Lazy loading**: Packs are loaded on first access
- **Inheritance resolution**: DFS traversal builds merged rule set
- **Cycle detection**: Prevents circular inheritance

```
nl/standard
    └── vlaams/basis
            ├── vlaams/west-vlaams
            │       └── vlaams/brugge
            │       └── vlaams/kortrijk
            ├── vlaams/antwerps
            ├── vlaams/limburgs
            │       └── vlaams/genk
            └── vlaams/brussels
```

### 3. Protected Terms System

Certain words must NEVER be transformed to avoid meaning drift:

**Global Protected Terms** (hardcoded in `transformer.py`):
- Legal modality: `verplicht`, `verboden`, `mag`, `moet`, `kan`
- Conditions: `tenzij`, `enkel`, `alleen`, `behalve`, `uitzondering`
- Penalties: `boete`, `straf`

**Pack-specific Protected Terms**: Each pack can define additional terms.

**Masking mechanism**:
1. Before transformation: protected terms → Unicode Private Use Area placeholders
2. After transformation: placeholders → original terms (verbatim)

## Rule Types

### `replace_word`

Simple whole-word replacement with case handling.

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

Options:
- `case_sensitive` (default: false) - Match case-insensitively
- `preserve_case` (default: true) - Maintain leading case of original
- `only_in_questions` (default: false) - Only apply in sentences ending with `?`

### `replace_regex`

Regex-based replacement for complex patterns.

```json
{
  "type": "replace_regex",
  "pattern": "\\bdat is\\b",
  "to": "da's",
  "flags": ["IGNORECASE"],
  "preserve_case": false
}
```

Options:
- `flags` - List of: `IGNORECASE`, `MULTILINE`
- `preserve_case` (default: false) - Only for simple replacements (no backrefs)

### `append_particle`

Adds discourse particles probabilistically.

```json
{
  "type": "append_particle",
  "particle": "zeg",
  "probability": 0.08,
  "positions": ["end_of_sentence"]
}
```

Notes:
- Only activated when `enable_particles=True` in config
- Deterministic by default (uses hash-based pseudo-random)
- Idempotent: won't double-append same particle

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VLAAMSCODEX_DIALECTS_DIR` | auto-detect | Override dialects directory location |
| `VLAAMSCODEX_DIALECT_DETERMINISTIC` | `true` | Deterministic transformations |
| `VLAAMSCODEX_DIALECT_SEED` | `0` | Seed for deterministic randomness |
| `VLAAMSCODEX_DIALECT_PARTICLES` | `false` | Enable particle appending |
| `VLAAMSCODEX_PRONOUN_SUBJECT` | `ge` | Subject pronoun in templates |
| `VLAAMSCODEX_PRONOUN_OBJECT` | `u` | Object pronoun in templates |
| `VLAAMSCODEX_PRONOUN_POSSESSIVE` | `uw` | Possessive pronoun in templates |
| `VLAAMSCODEX_DIALECT_MAX_PASSES` | `3` | Max transformation iterations |
| `VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY` | `false` | Error on non-convergence |

### Runtime Configuration

```python
transform(
    text,
    dialect_id,
    deterministic=True,
    seed=42,
    enable_particles=True,
    pronoun_subject="gij",
    pronoun_object="u",
    pronoun_possessive="uw",
    max_passes=3,
    strict_idempotency=False
)
```

## Pack Format

Packs are JSON files in `dialects/packs/`:

```json
{
  "id": "vlaams/antwerps",
  "label": "Antwerps",
  "inherits": ["vlaams/basis"],
  "notes": "Antwerp city dialect features",
  "protected_terms": ["specifiek", "term"],
  "rules": [
    {"type": "replace_word", "from": "goed", "to": "goe"},
    {"type": "replace_regex", "pattern": "\\bdat is\\b", "to": "da's", "flags": ["IGNORECASE"]},
    {"type": "append_particle", "particle": "zeg", "probability": 0.08, "positions": ["end_of_sentence"]}
  ]
}
```

### Pack Registry (`index.json`)

```json
[
  {
    "id": "vlaams/antwerps",
    "label": "Antwerps",
    "inherits": ["vlaams/basis"],
    "file": "vlaams__antwerps.json"
  }
]
```

## Inheritance Model

When a pack inherits from others:

1. **DFS traversal**: Parents are processed before children
2. **Rule accumulation**: All parent rules, then child rules
3. **Protected terms merge**: Union of all protected terms (deduplicated)
4. **No override**: Child rules don't replace parent rules, they append

Example inheritance chain:
```
nl/standard (base rules)
    ↓
vlaams/basis (common Flemish transforms)
    ↓
vlaams/antwerps (Antwerp-specific additions)
```

## Multi-Pass Transformation

The transformer runs multiple passes to handle cascading rules:

```python
# max_passes=3 by default
for pass in range(max_passes):
    new_text = apply_all_rules(text)
    if new_text == text:
        break  # Converged
    text = new_text
```

If `strict_idempotency=True` and text doesn't converge, raises `RuntimeError`.

## Development Tools

### Validate Packs

```bash
python tools/validate_dialect_packs.py
```

Checks:
- JSON syntax validity
- Required fields present
- ID matches filename convention
- Inheritance references exist
- No circular dependencies

### Generate Pack Scaffold

```bash
python tools/generate_dialect_packs.py
```

Creates starter pack JSON and updates index.

## Security Considerations

1. **No code execution**: Packs are pure data (JSON rules)
2. **Protected terms**: Legal/modality words are immutable
3. **Bounded iteration**: `max_passes` prevents infinite loops
4. **Deterministic**: Default behavior is reproducible

## Files

| File | Purpose |
|------|---------|
| `src/vlaamscodex/dialects/transformer.py` | Core transformation engine |
| `src/vlaamscodex/dialects/__init__.py` | Module exports |
| `dialects/index.json` | Pack registry |
| `dialects/packs/*.json` | Individual dialect packs (83+) |
| `dialects/schema.md` | Pack format specification |
| `dialects/README.md` | Pack documentation |
| `tools/validate_dialect_packs.py` | Validation utility |
| `tools/generate_dialect_packs.py` | Scaffold generator |
