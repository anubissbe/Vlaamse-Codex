# Maintenance Runbook

> Operations guide for maintaining VlaamsCodex.

## Health Checks

### Quick Health Check

```bash
# 1. Verify package installed
pip show vlaamscodex

# 2. Check CLI works
plats version

# 3. Verify codec registered
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"

# 4. Test magic mode
echo '# coding: vlaamsplats
plan doe
  klap tekst OK amen
gedaan' | python -

# 5. Check dialects available
plats dialecten | head -5
```

### Full Health Check

```bash
#!/bin/bash
# health_check.sh

echo "=== VlaamsCodex Health Check ==="

# Package version
echo -n "Version: "
plats version 2>/dev/null || echo "FAIL: CLI not found"

# Codec registration
echo -n "Codec: "
python -c "import codecs; codecs.lookup('vlaamsplats'); print('OK')" 2>/dev/null || echo "FAIL"

# CLI commands
for cmd in run build show-python repl examples check init fortune help; do
  echo -n "CLI $cmd: "
  plats $cmd --help >/dev/null 2>&1 && echo "OK" || echo "FAIL"
done

# Dialects
echo -n "Dialects: "
COUNT=$(plats dialecten 2>/dev/null | wc -l)
echo "$COUNT available"

# Magic mode
echo -n "Magic mode: "
echo '# coding: vlaamsplats
plan doe
  klap tekst OK amen
gedaan' > /tmp/health_test.plats
python /tmp/health_test.plats 2>/dev/null | grep -q OK && echo "OK" || echo "FAIL"
rm -f /tmp/health_test.plats

echo "=== Health Check Complete ==="
```

---

## Common Operations

### Upgrade Package

```bash
# Standard upgrade
pip install --upgrade vlaamscodex

# Force reinstall (if issues)
pip install --force-reinstall vlaamscodex

# Verify after upgrade
plats version
```

### Reinstall Clean

```bash
# Complete reinstall
pip uninstall vlaamscodex -y
pip cache purge
pip install vlaamscodex

# Verify
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
```

### Install from Source

```bash
git clone https://github.com/anubissbe/Vlaamse-Codex.git
cd Vlaamse-Codex
pip install -e ".[dev]"
```

---

## Troubleshooting Procedures

### Issue: Magic Mode Not Working

**Symptom:** `python script.plats` fails with encoding error.

**Diagnostic:**
```bash
# Check codec registration
python -c "import codecs; codecs.lookup('vlaamsplats')"

# Check .pth file exists
python -c "import site; print(site.getsitepackages()[0])"
ls $(python -c "import site; print(site.getsitepackages()[0])")/*.pth
```

**Resolution:**
```bash
# Reinstall package
pip install --force-reinstall vlaamscodex

# Or use CLI fallback
plats run script.plats
```

### Issue: Dialects Not Found

**Symptom:** "Could not find dialects directory" error.

**Diagnostic:**
```bash
# Check where dialects should be
python -c "import site; print(site.getsitepackages()[0] + '/dialects')"
ls $(python -c "import site; print(site.getsitepackages()[0])")/dialects/

# Check environment variable
echo $VLAAMSCODEX_DIALECTS_DIR
```

**Resolution:**
```bash
# Reinstall package
pip install --force-reinstall vlaamscodex

# Or set environment variable
export VLAAMSCODEX_DIALECTS_DIR=/path/to/dialects
```

### Issue: CLI Command Not Found

**Symptom:** `plats: command not found`

**Diagnostic:**
```bash
# Check if installed
pip show vlaamscodex

# Check entry point
pip show -f vlaamscodex | grep entry

# Find Python scripts directory
python -c "import site; print(site.USER_SITE)"
python -c "import sys; print(sys.prefix + '/bin')"
```

**Resolution:**
```bash
# Add to PATH
export PATH="$(python -c 'import site; print(site.USER_BASE)')/bin:$PATH"

# Or use module directly
python -m vlaamscodex.cli run script.plats
```

### Issue: Test Failures

**Symptom:** `pytest` fails after changes.

**Diagnostic:**
```bash
# Run with verbose output
pytest tests/ -v --tb=long

# Run single test
pytest tests/test_compiler.py::test_compile_plats_hello_shape -v

# Check for import issues
python -c "import vlaamscodex"
```

**Resolution:**
```bash
# Fresh install
pip install -e ".[dev]"

# Clear caches
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Rerun tests
pytest tests/ -v
```

---

## Monitoring

### Package Statistics

Track at:
- [PyPI Downloads](https://pypistats.org/packages/vlaamscodex)
- [GitHub Insights](https://github.com/anubissbe/Vlaamse-Codex/pulse)

### CI Status

Check workflow status:
- [CI Workflow](https://github.com/anubissbe/Vlaamse-Codex/actions/workflows/ci.yml)
- [Publish Workflow](https://github.com/anubissbe/Vlaamse-Codex/actions/workflows/publish.yml)

---

## Backup Procedures

### Code Backup

The primary backup is GitHub. For additional backup:

```bash
# Clone with full history
git clone --mirror https://github.com/anubissbe/Vlaamse-Codex.git

# Create archive
tar -czf vlaamscodex-backup-$(date +%Y%m%d).tar.gz Vlaamse-Codex.git
```

### Dialect Packs Backup

```bash
# Export all dialect packs
cp -r $(python -c "import site; print(site.getsitepackages()[0])")/dialects ./dialects-backup
```

---

## Dependency Updates

### Check Outdated

```bash
pip list --outdated | grep -E "setuptools|wheel|pytest|build"
```

### Update Dependencies

```bash
# Update build dependencies
pip install --upgrade setuptools wheel build

# Update dev dependencies
pip install --upgrade pytest

# Test after update
pytest tests/ -v
```

### Update GitHub Actions

Check for updates to:
- `actions/checkout`
- `actions/setup-python`
- `actions/upload-artifact`
- `softprops/action-gh-release`

---

## Performance Considerations

### Dialect Transformation

For high-volume usage:

1. **Cache registry:** The dialect registry is cached after first load
2. **Reuse config:** Create `DialectTransformConfig` once, reuse
3. **Batch processing:** Process multiple texts in sequence

```python
from vlaamscodex.dialects.transformer import transform

# Process batch
texts = ["text1", "text2", "text3"]
results = [transform(t, "antwerps") for t in texts]
```

### CLI Startup

The CLI has minimal startup overhead. For batch operations, use Python API directly instead of repeated CLI calls.

---

## Security Considerations

### Code Execution

- `.plats` files are code - treat as executable
- Don't run untrusted `.plats` files automatically
- Review dialect packs before adding custom ones

### CI/CD Secrets

- Rotate `PYPI_API_TOKEN` annually
- Use project-scoped tokens when possible
- Limit `VSCE_PAT` scope to Marketplace

### Dependency Auditing

```bash
# Check for known vulnerabilities
pip-audit

# Or use safety
pip install safety
safety check
```

---

## Incident Response

### Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P1 - Critical | Security vulnerability, data loss | Immediate |
| P2 - High | Major functionality broken | Within 24h |
| P3 - Medium | Feature broken, workaround exists | Within 1 week |
| P4 - Low | Minor issue, cosmetic | Next release |

### Response Procedure

1. **Assess severity** - Determine impact and scope
2. **Communicate** - Post issue on GitHub
3. **Investigate** - Identify root cause
4. **Fix** - Develop and test fix
5. **Release** - Emergency release if P1/P2
6. **Post-mortem** - Document lessons learned

### Emergency Release

For P1/P2 issues:

```bash
# Create hotfix branch
git checkout -b hotfix/v0.2.1

# Make fix
# ... fix the issue ...

# Test
pytest tests/ -v

# Fast-track release
git commit -am "fix: critical issue"
git push origin hotfix/v0.2.1

# Create PR, get expedited review, merge
# Tag and release immediately
```

---

## Useful Commands Reference

```bash
# Package info
pip show vlaamscodex
pip show -f vlaamscodex

# Check codec
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"

# Check dialects
plats dialecten

# Run tests
pytest tests/ -v

# Build package
python -m build

# Check wheel
unzip -l dist/*.whl | grep -E "pth|dialects"

# Clean build
rm -rf dist/ build/ *.egg-info

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```
