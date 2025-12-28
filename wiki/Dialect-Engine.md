# Dialect Engine

> Rule-based text transformation internals 🔧

This page documents the internal workings of the dialect transformer for developers who want to understand or extend it.

---

## Overview

The dialect transformer is a rule-based text transformation system that converts neutral Dutch text into various Flemish dialect styles.

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

---

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
    "antwerps",
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
algemeen-vlaams (base)
├── antwerps
│   ├── mechels
│   └── kempen-antwerps
├── west-vlaams
│   ├── brugs
│   └── kortrijks
├── limburgs
│   ├── hasselts
│   └── genks
└── brussels
```

### 3. Protected Terms System

Certain words must NEVER be transformed to avoid meaning drift.

**Global Protected Terms** (hardcoded in `transformer.py`):
- Legal modality: `verplicht`, `verboden`, `mag`, `moet`, `kan`
- Conditions: `tenzij`, `enkel`, `alleen`, `behalve`, `uitzondering`
- Penalties: `boete`, `straf`

**Pack-specific Protected Terms**: Each pack can define additional terms.

**Masking mechanism**:
1. Before transformation: protected terms → Unicode Private Use Area placeholders
2. After transformation: placeholders → original terms (verbatim)

---

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

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `case_sensitive` | `false` | Match case-insensitively |
| `preserve_case` | `true` | Maintain leading case of original |
| `only_in_questions` | `false` | Only apply in sentences ending with `?` |

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

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `flags` | `[]` | List of: `IGNORECASE`, `MULTILINE` |
| `preserve_case` | `false` | Only for simple replacements (no backrefs) |

**Safeguards:**
- Avoid patterns that can match across sentence boundaries (`.*`, DOTALL, etc.)

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

**Notes:**
- Only activated when `enable_particles=True` in config
- Deterministic by default (uses hash-based pseudo-random)
- Idempotent: won't double-append same particle

---

## Pack Format

Packs are JSON files in `dialects/packs/`:

```json
{
  "id": "antwerps",
  "label": "Antwerps",
  "inherits": ["algemeen-vlaams"],
  "notes": "Antwerp city dialect features",
  "protected_terms": ["specifiek", "term"],
  "rules": [
    {"type": "replace_word", "from": "goed", "to": "goe"},
    {"type": "replace_regex", "pattern": "\\bdat is\\b", "to": "da's", "flags": ["IGNORECASE"]},
    {"type": "append_particle", "particle": "zeg", "probability": 0.08, "positions": ["end_of_sentence"]}
  ]
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Stable pack identifier |
| `label` | string | Yes | Human-readable label |
| `inherits` | array | No | Parent pack IDs |
| `notes` | string | No | Free text (ignored by transformer) |
| `protected_terms` | array | Yes | Terms that must remain unchanged |
| `rules` | array | Yes | Ordered transformation rules |

### Pack Registry (`index.json`)

```json
[
  {
    "id": "antwerps",
    "label": "Antwerps",
    "inherits": ["algemeen-vlaams"],
    "file": "antwerps.json"
  }
]
```

---

## Inheritance Model

When a pack inherits from others:

1. **DFS traversal**: Parents are processed before children
2. **Rule accumulation**: All parent rules, then child rules
3. **Protected terms merge**: Union of all protected terms (deduplicated)
4. **No override**: Child rules don't replace parent rules, they append

### Example Inheritance Chain

```
algemeen-vlaams (base rules)
    ↓
antwerps (common Antwerp transforms)
    ↓
mechels (Mechelen-specific additions)
```

### Resolution Process

```python
def resolve_pack(pack_id):
    pack = load_pack(pack_id)
    rules = []
    protected = set()

    # Process parents first (DFS)
    for parent_id in pack.inherits:
        parent_rules, parent_protected = resolve_pack(parent_id)
        rules.extend(parent_rules)
        protected.update(parent_protected)

    # Then add this pack's rules
    rules.extend(pack.rules)
    protected.update(pack.protected_terms)

    return rules, protected
```

---

## Multi-Pass Transformation

The transformer runs multiple passes to handle cascading rules:

```python
# max_passes=3 by default
for pass_num in range(max_passes):
    new_text = apply_all_rules(text)
    if new_text == text:
        break  # Converged
    text = new_text
```

If `strict_idempotency=True` and text doesn't converge, raises `RuntimeError`.

### Why Multi-Pass?

Some rules create patterns matched by other rules:

```
"dat is goed"
→ "da's goed" (pass 1: "dat is" → "da's")
→ "da's goe"  (pass 2: "goed" → "goe")
```

---

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

---

## Replacement Variables

Some packs can use variables in `to`, written as `{var}`.

**Built-in variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `{pronoun_subject}` | `ge` | Subject pronoun |
| `{pronoun_object}` | `u` | Object pronoun |
| `{pronoun_possessive}` | `uw` | Possessive pronoun |

**Example:**

```json
{
  "type": "replace_word",
  "from": "jij",
  "to": "{pronoun_subject}"
}
```

---

## Development Tools

### Validate Packs

```bash
python tools/validate_dialect_packs.py
```

**Checks:**
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

---

## Security Considerations

1. **No code execution**: Packs are pure data (JSON rules)
2. **Protected terms**: Legal/modality words are immutable
3. **Bounded iteration**: `max_passes` prevents infinite loops
4. **Deterministic**: Default behavior is reproducible

---

## Files

| File | Purpose |
|------|---------|
| `src/vlaamscodex/dialects/transformer.py` | Core transformation engine |
| `src/vlaamscodex/dialects/__init__.py` | Module exports |
| `dialects/index.json` | Pack registry |
| `dialects/packs/*.json` | Individual dialect packs (84+) |
| `dialects/schema.md` | Pack format specification |
| `dialects/README.md` | Pack documentation |
| `tools/validate_dialect_packs.py` | Validation utility |
| `tools/generate_dialect_packs.py` | Scaffold generator |

---

## Testing the Engine

### Unit Tests

```python
def test_simple_word_replacement():
    result = transform("goed", "antwerps")
    assert result == "goe"

def test_protected_terms_preserved():
    result = transform("moet", "antwerps")
    assert result == "moet"  # Protected
```

### Integration Tests

```python
def test_inheritance_chain():
    result = transform("Dat is goed", "mechels")
    # Should apply both antwerps and mechels rules
    assert "Da's" in result or "da's" in result
```

---

## See Also

- [[Dialect-Guide]] - User documentation
- [[Creating-Dialect-Packs]] - How to create new packs
- [[API-Reference]] - Python API documentation
- [[Architecture-Overview]] - System design

---

**Veel plansen!** 🧇
