# Build and Release

> Building, packaging, and releasing VlaamsCodex 📦

This page documents the build system, versioning, and release process for VlaamsCodex maintainers and contributors.

---

## Overview

VlaamsCodex uses a **custom PEP 517 build backend** to handle special packaging requirements:

```
pyproject.toml → vlaamscodex_build_backend.py → setuptools → wheel
                         │
                         ├── Inject .pth file (startup hook)
                         └── Inject dialects/ directory
```

---

## Why a Custom Backend?

Standard Python packaging doesn't support:

1. **Startup hooks**: We need `.pth` files in `site-packages` root to register the codec before any `.plats` files are imported
2. **Non-package data**: The `dialects/` directory must be at `site-packages/dialects/`, not inside the package

---

## Build Commands

### Development Install

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
plats version
pytest tests/ -v
```

### Build Package

```bash
# Build wheel and source distribution
python -m build

# Output in dist/
ls dist/
# vlaamscodex-0.2.0-py3-none-any.whl
# vlaamscodex-0.2.0.tar.gz
```

### Build VS Code Extension

```bash
cd vscode-extension
npm install
npm run compile
npx @vscode/vsce package

# Output: vlaamscodex-platskript-0.2.0.vsix
```

---

## Build Backend Implementation

### pyproject.toml Configuration

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "vlaamscodex_build_backend"
backend-path = ["."]
```

- `build-backend`: Points to our custom module
- `backend-path`: Includes repo root so our module is importable

### Backend Module

**`vlaamscodex_build_backend.py`:**

```python
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
```

### Wheel Post-Processing

The `_ensure_autoload_pth_in_wheel()` function:

1. Opens wheel (ZIP archive)
2. Checks if `.pth` already present (idempotency)
3. Extracts to temp directory
4. Copies `data/vlaamscodex_autoload.pth` to wheel root
5. Copies `dialects/` directory to wheel root
6. Updates RECORD with new file hashes
7. Repacks wheel
8. Replaces original

---

## Wheel Contents

### Final Structure

```
vlaamscodex-0.2.0-py3-none-any.whl
├── vlaamscodex/                      # Python package
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
├── vlaamscodex_autoload.pth          # Injected startup hook
├── dialects/                         # Injected dialect packs
│   ├── index.json
│   └── packs/*.json (84 files)
└── vlaamscodex-0.2.0.dist-info/
    ├── METADATA
    ├── WHEEL
    ├── RECORD
    └── entry_points.txt
```

### Installation Result

```
site-packages/
├── vlaamscodex/              # Package
├── vlaamscodex_autoload.pth  # Startup hook (wheel root)
└── dialects/                 # Dialect packs (wheel root)
```

---

## The `.pth` Startup Hook

### File: `data/vlaamscodex_autoload.pth`

```python
import vlaamscodex.codec; vlaamscodex.codec.register()
```

### How It Works

1. Python's `site.py` reads all `.pth` files from `site-packages` at startup
2. Lines starting with `import` are executed
3. Our codec is registered before any user code runs
4. Now `# coding: vlaamsplats` works in any `.plats` file

---

## Version Management

### Three Locations

Version must be synchronized in:

| Location | Field | Format |
|----------|-------|--------|
| `src/vlaamscodex/__init__.py` | `__version__` | `"0.2.0"` |
| `pyproject.toml` | `project.version` | `"0.2.0"` |
| `vscode-extension/package.json` | `version` | `"0.2.0"` |

### Updating Version

```bash
# Update all three locations
# 1. src/vlaamscodex/__init__.py
# 2. pyproject.toml
# 3. vscode-extension/package.json

# Verify sync
python -c "import vlaamscodex; print(vlaamscodex.__version__)"
grep version pyproject.toml
grep version vscode-extension/package.json
```

---

## Release Process

### 1. Prepare Release

```bash
# Ensure clean working directory
git status

# Run all tests
pytest tests/ -v

# Validate dialect packs
python tools/validate_dialect_packs.py

# Update version in all locations
# (see Version Management above)

# Update CHANGELOG.md
```

### 2. Create Release Commit

```bash
git add -A
git commit -m "Release v0.2.0"
git tag v0.2.0
git push origin main --tags
```

### 3. Build Artifacts

```bash
# Python package
python -m build

# VS Code extension
cd vscode-extension
npm run compile
npx @vscode/vsce package
```

### 4. Publish

```bash
# PyPI (requires credentials)
twine upload dist/*

# VS Code Marketplace (requires PAT)
npx @vscode/vsce publish
```

### 5. Create GitHub Release

1. Go to GitHub Releases
2. Create new release from tag
3. Upload artifacts:
   - `vlaamscodex-X.Y.Z-py3-none-any.whl`
   - `vlaamscodex-X.Y.Z.tar.gz`
   - `vlaamscodex-platskript-X.Y.Z.vsix`
4. Write release notes

---

## CI/CD (GitHub Actions)

### Build Workflow

```yaml
# .github/workflows/build.yml
name: Build
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install build
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

---

## Testing the Build

### Verify Wheel Contents

```bash
# List contents
unzip -l dist/vlaamscodex-*.whl

# Verify .pth is present
unzip -p dist/vlaamscodex-*.whl vlaamscodex_autoload.pth

# Verify dialects
unzip -l dist/vlaamscodex-*.whl | grep dialects
```

### Test Installation

```bash
# Create test environment
python -m venv /tmp/test-env
source /tmp/test-env/bin/activate

# Install from wheel
pip install dist/vlaamscodex-*.whl

# Verify codec registration
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"

# Test CLI
plats version
plats run examples/hello.plats

# Test magic mode
echo '# coding: vlaamsplats
plan doe
  klap tekst test amen
gedaan' > /tmp/test.plats
python /tmp/test.plats
```

---

## Troubleshooting

### "Could not find dialects directory"

The dialects weren't installed. Check:

```bash
python -c "import site; print(site.getsitepackages())"
ls $(python -c "import site; print(site.getsitepackages()[0])")/dialects/
```

### Codec Not Registered

The `.pth` wasn't executed. Check:

```bash
ls $(python -c "import site; print(site.getsitepackages()[0])")/*.pth
```

### Wheel Build Fails

Ensure setuptools and wheel are current:

```bash
pip install --upgrade setuptools wheel build
```

### RECORD Hash Mismatch

The build backend updates RECORD. If errors persist:

```bash
# Clean and rebuild
rm -rf dist/ build/ *.egg-info
python -m build
```

---

## Development Dependencies

### pyproject.toml Dev Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "build",
    "twine",
]
```

### Install for Development

```bash
pip install -e ".[dev]"
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `pyproject.toml` | Package metadata and build config |
| `vlaamscodex_build_backend.py` | Custom build backend |
| `data/vlaamscodex_autoload.pth` | Codec startup hook |
| `src/vlaamscodex/__init__.py` | Version and exports |
| `CHANGELOG.md` | Release history |

---

## See Also

- [[Architecture-Overview]] - System design
- [[Magic-Mode]] - Codec and startup hook
- [[Contributing]] - Development workflow
- [[Troubleshooting]] - Common issues

---

**Veel plansen!** 🧇
