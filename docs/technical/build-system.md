# Build System Architecture

> Custom PEP 517 build backend for VlaamsCodex packaging.

## Overview

VlaamsCodex uses a **custom build backend** (`vlaamscodex_build_backend.py`) that wraps setuptools to inject additional files into wheels during the build process.

```
pyproject.toml ──▶ vlaamscodex_build_backend.py ──▶ setuptools ──▶ wheel
                           │
                           ├──▶ Inject .pth file
                           └──▶ Inject dialects/ directory
```

## Why a Custom Backend?

Standard Python packaging doesn't support:

1. **Startup hooks**: We need `.pth` files in `site-packages` root to register the codec before any `.plats` files are imported
2. **Non-package data**: The `dialects/` directory must be at `site-packages/dialects/`, not inside the package

## Implementation

### pyproject.toml Configuration

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "vlaamscodex_build_backend"
backend-path = ["."]
```

- `build-backend`: Points to our custom module
- `backend-path`: Includes repo root so our module is importable

### Backend Module Structure

```python
# vlaamscodex_build_backend.py

import setuptools.build_meta as _orig

def build_wheel(wheel_directory, config_settings, metadata_directory):
    # 1. Build wheel normally with setuptools
    filename = _orig.build_wheel(wheel_directory, config_settings, metadata_directory)

    # 2. Post-process: inject .pth and dialects
    _ensure_autoload_pth_in_wheel(Path(wheel_directory) / filename)

    return filename

def build_editable(...):
    # Same post-processing for editable installs
    ...

# Delegate other hooks to setuptools
get_requires_for_build_wheel = _orig.get_requires_for_build_wheel
prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel
# ... etc
```

## Wheel Post-Processing

### `_ensure_autoload_pth_in_wheel(wheel_path)`

This function modifies the wheel after setuptools creates it:

```
1. Open wheel (ZIP archive)
2. Check if .pth already present (idempotency)
3. Extract to temp directory
4. Copy data/vlaamscodex_autoload.pth to wheel root
5. Copy dialects/ directory to wheel root
6. Update RECORD with new file hashes
7. Repack wheel
8. Replace original
```

### RECORD File Update

Wheels contain a `RECORD` file listing all contents with SHA256 hashes:

```csv
vlaamscodex/__init__.py,sha256=...,1234
vlaamscodex/compiler.py,sha256=...,5678
...
```

We must update this when adding files:

```python
def _hash_file(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    digest = hashlib.sha256(data).digest()
    b64 = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return f"sha256={b64}", len(data)

# Add new entries
rows.append(["vlaamscodex_autoload.pth", digest, str(size)])
for file in dialects_files:
    rows.append([file, hash, size])
```

## The .pth Startup Hook

### File: `data/vlaamscodex_autoload.pth`

```python
import vlaamscodex.codec; vlaamscodex.codec.register()
```

### How It Works

1. Python's `site.py` reads all `.pth` files from `site-packages` at startup
2. Lines starting with `import` are executed
3. Our codec is registered before any user code runs
4. Now `# coding: vlaamsplats` works in any `.plats` file

### Installation Location

```
site-packages/
├── vlaamscodex/              # Package
│   ├── __init__.py
│   └── ...
├── vlaamscodex_autoload.pth  # Startup hook (wheel root)
└── dialects/                 # Dialect packs (wheel root)
    ├── index.json
    └── packs/*.json
```

## Build Artifacts

### Wheel Contents

```
vlaamscodex-0.2.0-py3-none-any.whl
├── vlaamscodex/
│   ├── __init__.py
│   ├── compiler.py
│   ├── codec.py
│   ├── cli.py
│   ├── repl.py
│   ├── checker.py
│   ├── examples.py
│   ├── fortune.py
│   ├── init.py
│   └── dialects/
│       └── transformer.py
├── vlaamscodex_autoload.pth      # Injected
├── dialects/                      # Injected
│   ├── index.json
│   └── packs/*.json (83 files)
└── vlaamscodex-0.2.0.dist-info/
    ├── METADATA
    ├── WHEEL
    └── RECORD
```

### Source Distribution

```
vlaamscodex-0.2.0.tar.gz
├── src/vlaamscodex/
├── dialects/
├── data/
├── pyproject.toml
├── vlaamscodex_build_backend.py
└── ...
```

## Editable Installs

For `pip install -e .`:

```python
def build_editable(wheel_directory, config_settings, metadata_directory):
    filename = _orig.build_editable(...)
    _ensure_autoload_pth_in_wheel(Path(wheel_directory) / filename)
    return filename
```

The `.pth` is injected into the editable wheel, pointing to the source directory.

## Testing the Build

```bash
# Build wheel and sdist
python -m build

# Inspect wheel contents
unzip -l dist/vlaamscodex-*.whl

# Verify .pth is present
unzip -p dist/vlaamscodex-*.whl vlaamscodex_autoload.pth

# Test installation
pip install dist/vlaamscodex-*.whl
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
```

## Troubleshooting

### "Could not find dialects directory"

The dialects weren't installed. Check:
```bash
python -c "import site; print(site.getsitepackages())"
ls $(python -c "import site; print(site.getsitepackages()[0])")/dialects/
```

### Codec not registered

The `.pth` wasn't executed. Check:
```bash
ls $(python -c "import site; print(site.getsitepackages()[0])")/*.pth
```

### Wheel build fails

Ensure setuptools and wheel are current:
```bash
pip install --upgrade setuptools wheel build
```
