# Configuration Reference

> All environment variables and configuration options.

## Environment Variables

### Dialect Transformer

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VLAAMSCODEX_DIALECTS_DIR` | Path | auto | Override dialect packs location |
| `VLAAMSCODEX_DIALECT_DETERMINISTIC` | bool | `True` | Enable deterministic mode |
| `VLAAMSCODEX_DIALECT_SEED` | int | `0` | Seed for deterministic randomness |
| `VLAAMSCODEX_DIALECT_PARTICLES` | bool | `False` | Enable particle insertion |
| `VLAAMSCODEX_DIALECT_MAX_PASSES` | int | `3` | Maximum transformation passes |
| `VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY` | bool | `False` | Raise on non-convergence |

### Pronoun Overrides

| Variable | Default | Description |
|----------|---------|-------------|
| `VLAAMSCODEX_PRONOUN_SUBJECT` | `ge` | Subject pronoun replacement |
| `VLAAMSCODEX_PRONOUN_OBJECT` | `u` | Object pronoun replacement |
| `VLAAMSCODEX_PRONOUN_POSSESSIVE` | `uw` | Possessive pronoun replacement |

---

## Dialect Configuration

### VLAAMSCODEX_DIALECTS_DIR

Override the location of dialect pack files.

```bash
export VLAAMSCODEX_DIALECTS_DIR=/path/to/custom/dialects
```

**Default lookup order:**
1. `VLAAMSCODEX_DIALECTS_DIR` environment variable
2. `site-packages/dialects/` (installed package)
3. `<repo>/dialects/` (development checkout)

**Use case:** Custom dialect packs for testing or local modifications.

### VLAAMSCODEX_DIALECT_DETERMINISTIC

Control whether transformations are reproducible.

```bash
# Enable (default)
export VLAAMSCODEX_DIALECT_DETERMINISTIC=True

# Disable for true randomness
export VLAAMSCODEX_DIALECT_DETERMINISTIC=False
```

**When enabled:**
- Same input + same seed = same output
- Good for CI/CD testing
- Predictable behavior

**When disabled:**
- Probabilistic rules vary each run
- More natural variation in output

### VLAAMSCODEX_DIALECT_SEED

Seed value for deterministic randomness.

```bash
export VLAAMSCODEX_DIALECT_SEED=42
```

**Range:** Any integer value.

**Use case:** Reproducible test fixtures.

### VLAAMSCODEX_DIALECT_PARTICLES

Enable insertion of characteristic dialect particles.

```bash
# Enable particles
export VLAAMSCODEX_DIALECT_PARTICLES=True
```

**Examples of particles:**
- Antwerps: `zansen`, `manneke`
- West-Vlaams: `jansen`, `zekers`
- Limburgs: `wansen`

**When disabled (default):** No particles are added, only word replacements.

### VLAAMSCODEX_DIALECT_MAX_PASSES

Maximum transformation iterations for convergence.

```bash
export VLAAMSCODEX_DIALECT_MAX_PASSES=5
```

**Default:** 3 passes

**Why multiple passes?**
Some rules create opportunities for other rules:
```
Pass 1: "gij hebt" → "ge hebt"
Pass 2: "ge hebt" → "g'ebt" (contraction)
```

### VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY

Raise error if transformation doesn't converge.

```bash
export VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY=True
```

**When enabled:**
- Raises `RuntimeError` if output keeps changing
- Useful for detecting rule conflicts

**When disabled (default):**
- Returns best-effort output
- Logs warning if non-convergent

---

## Pronoun Configuration

Override default pronoun replacements:

```bash
# Use "gij" instead of "ge" for subject
export VLAAMSCODEX_PRONOUN_SUBJECT=gij

# Use "jou" instead of "u" for object
export VLAAMSCODEX_PRONOUN_OBJECT=jou

# Use "jouwen" instead of "uw" for possessive
export VLAAMSCODEX_PRONOUN_POSSESSIVE=jouwen
```

**Use case:** Regional variations where default pronouns differ.

---

## VS Code Extension Configuration

### Settings

Access via: File → Preferences → Settings → Extensions → VlaamsCodex

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `vlaamscodex.platsPath` | string | `plats` | Path to `plats` CLI executable |

### Example settings.json

```json
{
  "vlaamscodex.platsPath": "/home/user/.local/bin/plats"
}
```

**Use case:** When `plats` is not in PATH or installed in non-standard location.

---

## Python Path Configuration

### Magic Mode Requirements

For magic mode (`python script.plats`) to work:

1. **Package must be installed:**
   ```bash
   pip install vlaamscodex
   ```

2. **Site module must be enabled:**
   ```bash
   # This works
   python script.plats

   # These break magic mode
   python -S script.plats   # Disables site
   python -I script.plats   # Isolated mode
   ```

3. **Codec must be registered:**
   ```bash
   python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
   ```

---

## CI/CD Configuration

### GitHub Actions Secrets

| Secret | Description | Required |
|--------|-------------|----------|
| `PYPI_API_TOKEN` | PyPI API token | For publishing |
| `VSCE_PAT` | VS Code Marketplace PAT | Optional |

### Setting PYPI_API_TOKEN

1. Go to [pypi.org/manage/account](https://pypi.org/manage/account/)
2. Create API token with scope "Entire account" or project-specific
3. Add to GitHub Secrets as `PYPI_API_TOKEN`

### Setting VSCE_PAT

1. Go to [Azure DevOps](https://dev.azure.com/)
2. Create Personal Access Token with "Marketplace (Manage)" scope
3. Add to GitHub Secrets as `VSCE_PAT`

---

## Configuration Precedence

Configuration sources are checked in order:

1. **Environment variables** (highest priority)
2. **Default values in code**

There are no config files - all configuration is via environment variables.

---

## Configuration Examples

### Development Environment

```bash
# Use local dialect packs
export VLAAMSCODEX_DIALECTS_DIR=./dialects

# Enable strict checking
export VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY=True

# Enable all features for testing
export VLAAMSCODEX_DIALECT_PARTICLES=True
```

### Production Environment

```bash
# Use deterministic mode (default)
export VLAAMSCODEX_DIALECT_DETERMINISTIC=True

# Fixed seed for consistency
export VLAAMSCODEX_DIALECT_SEED=12345

# Disable particles for clean output
export VLAAMSCODEX_DIALECT_PARTICLES=False
```

### CI/CD Environment

```bash
# Deterministic for reproducible tests
export VLAAMSCODEX_DIALECT_DETERMINISTIC=True
export VLAAMSCODEX_DIALECT_SEED=42

# Strict mode to catch issues
export VLAAMSCODEX_DIALECT_STRICT_IDEMPOTENCY=True
```

---

## Debugging Configuration

### Check Current Settings

```python
from vlaamscodex.dialects.transformer import _default_config

config = _default_config()
print(f"Deterministic: {config.deterministic}")
print(f"Seed: {config.seed}")
print(f"Particles: {config.enable_particles}")
print(f"Max passes: {config.max_passes}")
```

### Check Dialects Directory

```python
from vlaamscodex.dialects.transformer import _find_dialects_dir

print(_find_dialects_dir())
```

### List Available Packs

```bash
plats dialecten
```

---

## Boolean Value Parsing

Boolean environment variables accept:

| True values | False values |
|-------------|--------------|
| `true`, `True`, `TRUE` | `false`, `False`, `FALSE` |
| `1`, `yes`, `on` | `0`, `no`, `off` |

**Example:**
```bash
export VLAAMSCODEX_DIALECT_PARTICLES=yes  # True
export VLAAMSCODEX_DIALECT_PARTICLES=0    # False
```
