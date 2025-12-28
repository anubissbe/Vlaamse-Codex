# Dialect Transformation Engine

> Technical internals of the rule-based text transformation system.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         transform(text, dialect_id)                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   Registry   │───▶│   Resolver   │───▶│   Compiler   │          │
│  │  Load packs  │    │  Inheritance │    │  Build rules │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│         │                   │                   │                   │
│         ▼                   ▼                   ▼                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ index.json   │    │ Flattened    │    │  Callable    │          │
│  │ packs/*.json │    │ rule chain   │    │  functions   │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                  │                   │
│                                                  ▼                   │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │                   Apply Transform                         │      │
│  │  1. Mask protected terms                                  │      │
│  │  2. Apply rules sequentially                              │      │
│  │  3. Unmask protected terms                                │      │
│  │  4. Repeat until convergence (max_passes)                 │      │
│  └──────────────────────────────────────────────────────────┘      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Core Components

### `_DialectRegistry`

Manages pack discovery, loading, and caching:

```python
class _DialectRegistry:
    def __init__(self, dialects_dir: Path | None = None):
        self.dialects_dir = dialects_dir or _find_dialects_dir()
        self.index_path = self.dialects_dir / "index.json"
        self.packs_dir = self.dialects_dir / "packs"
        self._index: dict | None = None      # Lazy-loaded
        self._loaded: dict[str, _LoadedPack] = {}   # Cache
        self._resolved: dict[str, _ResolvedPack] = {}  # Cache

    def available(self) -> list[PackInfo]:
        """List all registered dialect packs."""

    def load(self, dialect_id: str) -> _LoadedPack:
        """Load a single pack from disk (with caching)."""

    def resolve(self, dialect_id: str) -> _ResolvedPack:
        """Resolve inheritance chain into flattened pack."""
```

### Data Classes

```python
@dataclass(frozen=True, slots=True)
class PackInfo:
    """Public metadata about a pack."""
    id: str
    label: str
    inherits: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class _LoadedPack:
    """Internal: single pack as loaded from JSON."""
    id: str
    label: str
    inherits: tuple[str, ...]
    protected_terms: tuple[str, ...]
    rules: tuple[dict[str, Any], ...]

@dataclass(frozen=True, slots=True)
class _ResolvedPack:
    """Internal: pack with inherited rules merged."""
    id: str
    label: str
    inherits: tuple[str, ...]
    protected_terms: tuple[str, ...]
    rules: tuple[dict[str, Any], ...]  # Flattened from ancestors
```

## Inheritance Resolution

### DFS Topological Sort

```python
def resolve(self, dialect_id: str) -> _ResolvedPack:
    visiting: set[str] = set()  # Cycle detection
    order: list[str] = []       # Topological order
    visited: set[str] = set()

    def dfs(pid: str):
        if pid in visited:
            return
        if pid in visiting:
            raise ValueError(f"Cycle detected: {' -> '.join([*visiting, pid])}")

        visiting.add(pid)
        pack = self.load(pid)

        # Process parents first
        for parent in pack.inherits:
            dfs(parent)

        visiting.remove(pid)
        visited.add(pid)
        order.append(pid)  # Children after parents

    dfs(dialect_id)

    # Merge rules: parents first, then child (overrides)
    rules = []
    for pid in order:
        rules.extend(self.load(pid).rules)

    return _ResolvedPack(id=dialect_id, ..., rules=tuple(rules))
```

### Example Inheritance

```
antwerps/haven
  └── inherits: antwerps
        └── inherits: algemeen-vlaams
```

Resolution order: `[algemeen-vlaams, antwerps, antwerps/haven]`

Rules apply in this order, so more specific dialects override general ones.

## Rule Types

### `replace_word`

Simple word-boundary replacement:

```json
{
  "type": "replace_word",
  "from": "gij",
  "to": "ge",
  "case_sensitive": false,
  "preserve_case": true,
  "only_in_questions": false
}
```

Compiled to:

```python
pat = re.compile(r"\bgij\b", flags=re.IGNORECASE)

def apply(text):
    if preserve_case:
        return pat.sub(lambda m: _apply_leading_case("ge", m.group(0)), text)
    return pat.sub("ge", text)
```

### `replace_regex`

Full regex pattern replacement:

```json
{
  "type": "replace_regex",
  "pattern": "\\bdat\\b",
  "to": "da",
  "flags": ["IGNORECASE"],
  "preserve_case": true
}
```

Compiled to:

```python
pat = re.compile(r"\bdat\b", flags=re.IGNORECASE)

def apply(text):
    return pat.sub(lambda m: _apply_leading_case("da", m.group(0)), text)
```

### `append_particle`

Probabilistic particle insertion at sentence ends:

```json
{
  "type": "append_particle",
  "particle": "zansen",
  "probability": 0.3,
  "positions": ["end_of_sentence"]
}
```

Compiled to:

```python
def apply(text):
    if not config.enable_particles:
        return text

    result = []
    for start, end, is_question in _iter_sentence_spans(text):
        chunk = text[start:end]

        # Skip if already has particle or no punctuation
        if already_pat.search(chunk) or not punct_pat.search(chunk):
            result.append(chunk)
            continue

        # Probabilistic insertion
        if probability < 1:
            key = f"{seed}|{dialect_id}|append_particle|{sent_i}"
            if _hash_float_0_1(key) >= probability:
                result.append(chunk)
                continue

        # Insert particle before punctuation
        chunk = punct_pat.sub(rf", {particle}\1", chunk)
        result.append(chunk)

    return "".join(result)
```

## Protected Terms System

### Global Protected Terms

Words that are **never** transformed (legal/modality):

```python
GLOBAL_PROTECTED_TERMS = (
    "verplicht", "verboden", "mag", "moet", "kan",
    "niet", "geen", "tenzij", "enkel", "alleen",
    "behalve", "uitzondering", "boete", "straf",
    "uitzonderingen", "boetes", "straffen",
)
```

### Masking Algorithm

```python
def _mask_protected(text: str, terms: Iterable[str]) -> tuple[str, dict[str, str]]:
    """Replace protected terms with placeholders."""
    pat = _build_protected_pattern(terms)  # Compile regex

    mapping = {}
    counter = 0

    def repl(m):
        nonlocal counter
        placeholder = f"\uE000{counter}\uE001"  # Private use area
        mapping[placeholder] = m.group(0)
        counter += 1
        return placeholder

    masked = pat.sub(repl, text)
    return masked, mapping

def _unmask(text: str, mapping: dict[str, str]) -> str:
    """Restore protected terms from placeholders."""
    for placeholder, original in mapping.items():
        text = text.replace(placeholder, original)
    return text
```

### Why Private Use Area?

Unicode codepoints `\uE000`-`\uF8FF` are "private use" and:
- Never appear in normal text
- Won't be matched by any replacement rules
- Safe delimiters for our placeholders

## Transformation Loop

### Multi-pass Convergence

```python
def transform(text, dialect_id, **kwargs):
    config = _build_config(kwargs)
    resolved = registry.resolve(dialect_id)

    # Compile all rules into callables
    compiled_rules = [_compile_rule(r, config, dialect_id, i)
                      for i, r in enumerate(resolved.rules)]

    protected = (*GLOBAL_PROTECTED_TERMS, *resolved.protected_terms)

    def apply_once(src):
        masked, mapping = _mask_protected(src, protected)
        out = masked
        for fn in compiled_rules:
            out = fn(out)
        return _unmask(out, mapping)

    # Iterate until stable
    out = text
    seen = {out}
    for _ in range(config.max_passes):
        new = apply_once(out)
        if new == out:  # Converged
            return out
        if new in seen:  # Cycle detected
            break
        seen.add(new)
        out = new

    if config.strict_idempotency and apply_once(out) != out:
        raise RuntimeError(f"Transform did not converge for {dialect_id}")

    return out
```

### Why Multiple Passes?

Some rules may create opportunities for other rules:

```
Pass 1: "gij hebt" → "ge hebt"
Pass 2: "ge hebt" → "g'ebt" (contraction rule)
```

Default `max_passes=3` handles most cascades.

## Deterministic Mode

### Hash-based Randomness

For reproducible probabilistic operations:

```python
def _hash_float_0_1(key: str) -> float:
    """Convert string to float in [0, 1) deterministically."""
    h = hashlib.sha256(key.encode("utf-8")).digest()
    x = int.from_bytes(h[:8], "big", signed=False)
    return x / 2**64
```

### Usage in Particle Insertion

```python
# Unique key per sentence position
key = f"{config.seed}|{dialect_id}|append_particle|{rule_index}|{sent_i}|{chunk}"
if _hash_float_0_1(key) >= probability:
    # Skip this insertion
    continue
```

This ensures:
- Same input + same seed = same output
- Different seeds = different outputs
- CI tests are reproducible

## Configuration

### Environment Variables

```python
VLAAMSCODEX_DIALECTS_DIR       # Override pack location
VLAAMSCODEX_DIALECT_DETERMINISTIC  # True/False
VLAAMSCODEX_DIALECT_SEED       # Integer seed
VLAAMSCODEX_DIALECT_PARTICLES  # Enable particle insertion
VLAAMSCODEX_PRONOUN_SUBJECT    # Default: "ge"
VLAAMSCODEX_PRONOUN_OBJECT     # Default: "u"
VLAAMSCODEX_PRONOUN_POSSESSIVE # Default: "uw"
VLAAMSCODEX_DIALECT_MAX_PASSES # Default: 3
VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY  # Raise on non-convergence
```

### Pronoun Variables in Rules

Rules can reference config pronouns:

```json
{
  "type": "replace_word",
  "from": "jullie",
  "to": "{pronoun_subject}lansen"
}
```

Expanded at compile time based on config.

## Performance Considerations

1. **Caching**: Registry caches loaded and resolved packs
2. **Compiled rules**: Regex patterns compiled once, reused
3. **Early exit**: Convergence check avoids unnecessary passes
4. **Lazy loading**: Packs only loaded when first used

For batch processing, reuse the same transform call with different texts.
