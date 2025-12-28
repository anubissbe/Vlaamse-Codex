# Deployment Guide

> Packaging, distribution, and deployment procedures.

## Package Distribution

### PyPI (Primary)

VlaamsCodex is distributed via [PyPI](https://pypi.org/project/vlaamscodex/).

```bash
# Users install with:
pip install vlaamscodex

# Or with pipx for isolated CLI:
pipx install vlaamscodex
```

### GitHub Releases

Each release includes downloadable artifacts:
- Wheel (`.whl`) - Binary distribution
- Source distribution (`.tar.gz`)
- VS Code extension (`.vsix`)

### VS Code Marketplace

Extension available at: [VlaamsCodex Platskript](https://marketplace.visualstudio.com/items?itemName=PlatsVlaamseCodex.vlaamscodex-platskript)

---

## Building Packages

### Prerequisites

```bash
pip install build twine
```

### Build Python Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel and sdist
python -m build

# Verify contents
ls -la dist/
# vlaamscodex-0.2.0-py3-none-any.whl
# vlaamscodex-0.2.0.tar.gz
```

### Verify Wheel Contents

```bash
# List wheel contents
unzip -l dist/vlaamscodex-*.whl

# Verify .pth file is included
unzip -l dist/vlaamscodex-*.whl | grep pth
# vlaamscodex_autoload.pth

# Verify dialects are included
unzip -l dist/vlaamscodex-*.whl | grep dialects/
# dialects/index.json
# dialects/packs/...
```

### Check Package Metadata

```bash
twine check dist/*
# Checking dist/vlaamscodex-0.2.0-py3-none-any.whl: PASSED
# Checking dist/vlaamscodex-0.2.0.tar.gz: PASSED
```

---

## Build VS Code Extension

### Prerequisites

```bash
cd vscode-extension
npm install
```

### Build Extension

```bash
# Compile TypeScript
npm run compile

# Package VSIX
npx @vscode/vsce package

# Result: vlaamscodex-platskript-0.2.0.vsix
```

### Verify Extension

```bash
# List contents
unzip -l *.vsix

# Install locally for testing
code --install-extension vlaamscodex-platskript-0.2.0.vsix
```

---

## Publishing

### Publish to PyPI

#### Test PyPI (Recommended First)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ vlaamscodex
```

#### Production PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Or with explicit credentials
TWINE_USERNAME=__token__ TWINE_PASSWORD=$PYPI_TOKEN twine upload dist/*
```

### Publish VS Code Extension

```bash
cd vscode-extension

# Publish to Marketplace
npx @vscode/vsce publish --pat $VSCE_PAT

# Or publish pre-packaged VSIX
npx @vscode/vsce publish --packagePath ./vlaamscodex-platskript-*.vsix --pat $VSCE_PAT
```

---

## Automated CI/CD

### Trigger Conditions

| Workflow | Trigger | Actions |
|----------|---------|---------|
| `ci.yml` | Push/PR to main | Run tests on Python 3.10-3.12 |
| `publish.yml` | GitHub Release published | Build + publish everything |

### Publish Workflow Jobs

```yaml
jobs:
  build:              # Build Python wheel/sdist
  build-vscode:       # Build VSIX
  publish-pypi:       # Upload to PyPI
  publish-github:     # Attach to release
```

### Required Secrets

| Secret | Used By | Required |
|--------|---------|----------|
| `PYPI_API_TOKEN` | publish-pypi | Yes |
| `VSCE_PAT` | build-vscode | Optional |
| `GITHUB_TOKEN` | publish-github | Auto-provided |

---

## Installation Methods

### Standard pip

```bash
pip install vlaamscodex
```

**Result:**
- Package in `site-packages/vlaamscodex/`
- `.pth` file in `site-packages/vlaamscodex_autoload.pth`
- Dialects in `site-packages/dialects/`
- CLI entry point `plats` in PATH

### pipx (Isolated)

```bash
pipx install vlaamscodex
```

**Benefits:**
- Isolated environment
- CLI always available
- Easy upgrades/uninstalls

### Development Install

```bash
git clone https://github.com/anubissbe/Vlaamse-Codex.git
cd Vlaamse-Codex
pip install -e ".[dev]"
```

**Result:**
- Editable install (code changes take effect immediately)
- Dev dependencies included

---

## Wheel Structure

The custom build backend produces:

```
vlaamscodex-0.2.0-py3-none-any.whl
├── vlaamscodex/
│   ├── __init__.py
│   ├── cli.py
│   ├── compiler.py
│   ├── codec.py
│   ├── repl.py
│   ├── checker.py
│   ├── fortune.py
│   ├── init.py
│   ├── examples.py
│   └── dialects/
│       └── transformer.py
├── vlaamscodex_autoload.pth     # Magic mode hook
├── dialects/                     # Dialect packs
│   ├── index.json
│   └── packs/
│       ├── algemeen-vlaams.json
│       ├── antwerps.json
│       └── ... (80+ files)
└── vlaamscodex-0.2.0.dist-info/
    ├── METADATA
    ├── WHEEL
    ├── RECORD
    └── entry_points.txt
```

### Special Files

| File | Purpose |
|------|---------|
| `vlaamscodex_autoload.pth` | Registers codec at Python startup |
| `dialects/` | Dialect pack data (at site-packages root) |
| `entry_points.txt` | Defines `plats` CLI command |

---

## Verification Checklist

After deployment, verify:

### 1. Package Installation

```bash
pip install vlaamscodex
pip show vlaamscodex
```

### 2. Codec Registration

```bash
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
```

### 3. CLI Functionality

```bash
plats version
plats help
plats examples --list
```

### 4. Magic Mode

```bash
echo '# coding: vlaamsplats
plan doe
  klap tekst test amen
gedaan' > /tmp/test.plats

python /tmp/test.plats
# Output: test
```

### 5. Dialect Transformation

```bash
plats dialecten | head -10
plats vraag "Dit is een test." --dialect antwerps
```

---

## Troubleshooting

### Wheel Missing .pth File

**Symptom:** Magic mode doesn't work after installation.

**Cause:** Build backend didn't inject `.pth` file.

**Fix:**
```bash
# Rebuild cleanly
rm -rf dist/ build/
python -m build

# Verify
unzip -l dist/*.whl | grep pth
```

### PyPI Upload Fails

**Symptom:** `twine upload` returns error.

**Common causes:**
- Invalid API token
- Version already exists
- Package metadata issues

**Fix:**
```bash
# Check package
twine check dist/*

# Use correct token
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-xxx twine upload dist/*
```

### VS Code Extension Not Publishing

**Symptom:** VSCE returns auth error.

**Fix:**
1. Regenerate PAT at [Azure DevOps](https://dev.azure.com/)
2. Ensure PAT has "Marketplace (Manage)" scope
3. Update `VSCE_PAT` secret

---

## Deployment Environments

### Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

### Staging (Test PyPI)

```bash
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ vlaamscodex
```

### Production (PyPI)

```bash
twine upload dist/*
pip install vlaamscodex
```
