# Release Process

> Complete guide to releasing new versions of VlaamsCodex.

## Version Management

### Version Locations

The version appears in **three files** that must stay synchronized:

| File | Pattern | Example |
|------|---------|---------|
| `src/vlaamscodex/__init__.py` | `__version__ = "X.Y.Z"` | `__version__ = "0.2.0"` |
| `pyproject.toml` | `version = "X.Y.Z"` | `version = "0.2.0"` |
| `vscode-extension/package.json` | `"version": "X.Y.Z"` | `"version": "0.2.0"` |

### Versioning Scheme

We follow [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes to public API
MINOR: New features, backward compatible
PATCH: Bug fixes, backward compatible
```

**Examples:**
- `0.2.0` → `0.3.0`: New dialect pack or CLI command
- `0.2.0` → `0.2.1`: Bug fix in transpiler
- `0.2.0` → `1.0.0`: Breaking change to language syntax

---

## Release Procedure

### 1. Pre-Release Checklist

```bash
# Ensure clean working directory
git status

# Pull latest main
git checkout main
git pull origin main

# Run full test suite
pytest tests/ -v

# Verify package builds
python -m build

# Test installation
pip install dist/vlaamscodex-*.whl
plats version
```

### 2. Update Version

Edit all three files:

**`src/vlaamscodex/__init__.py`:**
```python
__version__ = "0.3.0"  # New version
```

**`pyproject.toml`:**
```toml
version = "0.3.0"
```

**`vscode-extension/package.json`:**
```json
"version": "0.3.0"
```

### 3. Update CHANGELOG.md

Add entry at the top:

```markdown
## [0.3.0] - 2025-01-15

### Added
- New feature X
- Support for Y

### Changed
- Improved Z behavior

### Fixed
- Bug in A
- Issue with B

### Deprecated
- Feature C (will be removed in 1.0)
```

### 4. Create Release PR

```bash
# Create release branch
git checkout -b release/v0.3.0

# Commit changes
git add .
git commit -m "chore: bump version to 0.3.0"

# Push and create PR
git push origin release/v0.3.0
```

Create PR titled: `Release v0.3.0`

### 5. Merge and Tag

After PR is approved and merged:

```bash
# Pull merged changes
git checkout main
git pull origin main

# Create annotated tag
git tag -a v0.3.0 -m "Release v0.3.0"

# Push tag
git push origin v0.3.0
```

### 6. Create GitHub Release

1. Go to [Releases](https://github.com/anubissbe/Vlaamse-Codex/releases)
2. Click "Create a new release"
3. Select tag `v0.3.0`
4. Title: `VlaamsCodex v0.3.0`
5. Description: Copy from CHANGELOG
6. Click "Publish release"

### 7. Automated Publishing

The `publish.yml` workflow automatically:

1. **Builds Python package** (wheel + sdist)
2. **Builds VS Code extension** (VSIX)
3. **Publishes to PyPI** (if `PYPI_API_TOKEN` set)
4. **Publishes to VS Code Marketplace** (if `VSCE_PAT` set)
5. **Attaches artifacts to GitHub Release**

---

## CI/CD Secrets

### Required Secrets

| Secret | Purpose | How to Obtain |
|--------|---------|---------------|
| `PYPI_API_TOKEN` | Publish to PyPI | [pypi.org/manage/account](https://pypi.org/manage/account/) → API tokens |
| `VSCE_PAT` | Publish to VS Code Marketplace | [Azure DevOps PAT](https://code.visualstudio.com/api/working-with-extensions/publishing-extension#get-a-personal-access-token) |

### Setting Secrets

1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value

---

## Release Artifacts

Each release produces:

| Artifact | Filename | Destination |
|----------|----------|-------------|
| Wheel | `vlaamscodex-X.Y.Z-py3-none-any.whl` | PyPI, GitHub Release |
| Source dist | `vlaamscodex-X.Y.Z.tar.gz` | PyPI, GitHub Release |
| VS Code ext | `vlaamscodex-platskript-X.Y.Z.vsix` | GitHub Release, Marketplace |

---

## Rollback Procedure

If a release has critical issues:

### 1. Yank from PyPI

```bash
# Yank version (prevents new installs, existing installs work)
pip install twine
twine yank vlaamscodex X.Y.Z
```

### 2. Delete GitHub Release

1. Go to Releases
2. Click on the problematic release
3. Click "Delete release"

### 3. Delete Git Tag

```bash
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z
```

### 4. Create Hotfix

```bash
git checkout main
# Fix the issue
git commit -m "fix: critical issue in X.Y.Z"
# Release X.Y.Z+1
```

---

## Post-Release Verification

### Verify PyPI

```bash
# Check package is available
pip index versions vlaamscodex

# Install and test
pip install --upgrade vlaamscodex
plats version
```

### Verify GitHub Release

1. Check assets are attached (wheel, sdist, vsix)
2. Verify download links work

### Verify VS Code Marketplace

1. Search "VlaamsCodex" in VS Code Extensions
2. Verify version matches
3. Test installation

---

## Emergency Hotfix

For critical security or stability issues:

### Fast-Track Process

```bash
# Create hotfix from main
git checkout main
git checkout -b hotfix/v0.3.1

# Make minimal fix
vim src/vlaamscodex/xxx.py
pytest tests/ -v

# Commit
git commit -am "fix: critical security issue in X"

# Push and create PR (request expedited review)
git push origin hotfix/v0.3.1
```

### Expedited Release

1. Get single reviewer approval
2. Merge immediately
3. Tag and release within 24 hours
4. Notify users via GitHub Release notes

---

## Release Schedule

**No fixed schedule** - releases when:

- New features are ready
- Critical bugs are fixed
- Security issues are discovered
- Dependencies need updates

**Recommended**: At least one release per quarter to keep project active.

---

## Checklist Template

```markdown
## Release v0.X.Y Checklist

### Pre-Release
- [ ] All tests passing
- [ ] Package builds successfully
- [ ] Manual testing completed

### Version Updates
- [ ] `src/vlaamscodex/__init__.py`
- [ ] `pyproject.toml`
- [ ] `vscode-extension/package.json`
- [ ] `CHANGELOG.md`

### Release
- [ ] PR created and approved
- [ ] PR merged to main
- [ ] Tag created and pushed
- [ ] GitHub Release created

### Post-Release
- [ ] PyPI package verified
- [ ] GitHub assets verified
- [ ] VS Code extension verified (if applicable)
- [ ] Announcement posted (if major release)
```
