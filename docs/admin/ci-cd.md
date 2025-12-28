# CI/CD Pipeline

> GitHub Actions workflows for testing and publishing.

## Overview

VlaamsCodex uses two GitHub Actions workflows:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push/PR to main | Run tests across Python versions |
| `publish.yml` | GitHub Release | Build and publish packages |

---

## CI Workflow

**File:** `.github/workflows/ci.yml`

### Trigger

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

Runs on:
- Every push to `main`
- Every PR targeting `main`

### Jobs

#### test

Runs tests on multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

**Steps:**
1. Checkout code
2. Setup Python
3. Install package with dev dependencies
4. Run pytest

### Status Badge

Add to README:

```markdown
![CI](https://github.com/anubissbe/Vlaamse-Codex/actions/workflows/ci.yml/badge.svg)
```

---

## Publish Workflow

**File:** `.github/workflows/publish.yml`

### Trigger

```yaml
on:
  release:
    types: [published]
```

Runs when a GitHub Release is published.

### Jobs

#### build

Builds Python package:

1. Checkout code
2. Setup Python 3.11
3. Install build dependencies
4. Build wheel and sdist
5. Check with twine
6. Upload artifacts

**Output:** `dist/` artifact containing:
- `vlaamscodex-X.Y.Z-py3-none-any.whl`
- `vlaamscodex-X.Y.Z.tar.gz`

#### build-vscode-extension

Builds VS Code extension:

1. Checkout code
2. Setup Node.js 20
3. Extract version from release tag
4. Update package.json version
5. Install npm dependencies
6. Compile TypeScript
7. Package VSIX
8. Upload artifact
9. (Optional) Publish to Marketplace

**Output:** `vsix/` artifact containing:
- `vlaamscodex-platskript-X.Y.Z.vsix`

#### publish-pypi

Publishes to PyPI:

1. Download build artifacts
2. Setup Python
3. Install twine
4. Upload to PyPI

**Requires:** `PYPI_API_TOKEN` secret

#### publish-github-release

Attaches artifacts to release:

1. Download all artifacts
2. Upload to GitHub Release

**Uploads:**
- `dist/*.whl`
- `dist/*.tar.gz`
- `vsix/*.vsix`

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Release Published                 │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
      ┌──────────────┐               ┌──────────────────┐
      │    build     │               │ build-vscode-ext │
      │  (Python)    │               │   (Node.js)      │
      └──────────────┘               └──────────────────┘
              │                               │
              │ dist/ artifact                │ vsix/ artifact
              ▼                               │
      ┌──────────────┐                        │
      │ publish-pypi │                        │
      └──────────────┘                        │
              │                               │
              └───────────────┬───────────────┘
                              ▼
                 ┌─────────────────────────┐
                 │ publish-github-release  │
                 │ (attach all artifacts)  │
                 └─────────────────────────┘
```

---

## Required Secrets

### PYPI_API_TOKEN

**Purpose:** Authenticate with PyPI for publishing.

**How to obtain:**
1. Go to [pypi.org/manage/account](https://pypi.org/manage/account/)
2. Click "Add API token"
3. Name: "GitHub Actions"
4. Scope: "Entire account" or project-specific
5. Copy token

**How to set:**
1. Go to repository → Settings → Secrets → Actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Paste token

### VSCE_PAT (Optional)

**Purpose:** Publish VS Code extension to Marketplace.

**How to obtain:**
1. Go to [Azure DevOps](https://dev.azure.com/)
2. User settings → Personal access tokens
3. New Token with:
   - Organization: "All accessible organizations"
   - Scope: "Marketplace (Manage)"
4. Copy token

**How to set:**
1. Go to repository → Settings → Secrets → Actions
2. Click "New repository secret"
3. Name: `VSCE_PAT`
4. Value: Paste token

### GITHUB_TOKEN (Automatic)

Automatically provided by GitHub Actions. Used for:
- Uploading release assets
- Git operations within workflow

---

## Customization

### Adding Python Version

Edit `ci.yml`:

```yaml
matrix:
  python-version: ["3.10", "3.11", "3.12", "3.13"]
```

### Changing Test Command

Edit `ci.yml`:

```yaml
- name: Run tests
  run: pytest tests/ -v --cov=vlaamscodex
```

### Skip Publishing to Marketplace

The workflow checks if `VSCE_PAT` is set:

```yaml
- name: Publish to VS Code Marketplace
  if: ${{ secrets.VSCE_PAT != '' }}
  ...
```

If not set, this step is skipped.

---

## Debugging Workflows

### View Logs

1. Go to Actions tab
2. Click on workflow run
3. Click on job
4. Expand steps to see logs

### Re-run Failed Jobs

1. Go to failed workflow run
2. Click "Re-run jobs"
3. Choose "Re-run failed jobs" or "Re-run all jobs"

### Test Locally

Use [act](https://github.com/nektos/act) to run workflows locally:

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run CI workflow
act push

# Run with secrets
act push --secret-file .secrets
```

---

## Workflow Maintenance

### Keep Actions Updated

Periodically update action versions:

```yaml
# Check for updates
- uses: actions/checkout@v4      # Check for v5
- uses: actions/setup-python@v5  # Check for v6
```

### Monitor for Deprecations

GitHub announces deprecations. Watch for:
- Node.js version requirements
- Ubuntu runner changes
- Action version deprecations

### Review Run Times

Optimize if builds are slow:
- Cache pip dependencies
- Parallelize where possible
- Use matrix builds efficiently

---

## Branch Protection

Recommended settings for `main`:

1. Go to Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Status check: "test"
4. Save

This ensures:
- All PRs must pass CI
- Main branch is always in good state
- Tests run before merge

---

## Workflow Files Reference

### ci.yml

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v
```

### publish.yml (summary)

```yaml
name: Publish Package

on:
  release:
    types: [published]

jobs:
  build:           # Build Python package
  build-vscode:    # Build VSIX
  publish-pypi:    # Upload to PyPI
  publish-github:  # Attach to release
```

See `.github/workflows/publish.yml` for full details.
