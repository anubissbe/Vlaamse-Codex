# Admin & Operations Documentation

> Guides for maintainers, operators, and project administrators.

## Documentation

| Document | Description |
|----------|-------------|
| [Release Process](release-process.md) | Version management and release procedures |
| [Deployment Guide](deployment.md) | Packaging, PyPI, and distribution |
| [Configuration](configuration.md) | Environment variables and settings |
| [Maintenance Runbook](maintenance.md) | Operations, troubleshooting, and health checks |
| [CI/CD Pipeline](ci-cd.md) | GitHub Actions and automation |

## Quick Reference

### Version Locations

Version must be synchronized across three files:

| File | Location |
|------|----------|
| `src/vlaamscodex/__init__.py` | `__version__ = "0.2.0"` |
| `pyproject.toml` | `version = "0.2.0"` |
| `vscode-extension/package.json` | `"version": "0.2.0"` |

### Key Secrets Required

| Secret | Purpose | Where to Set |
|--------|---------|--------------|
| `PYPI_API_TOKEN` | PyPI publishing | GitHub Secrets |
| `VSCE_PAT` | VS Code Marketplace | GitHub Secrets (optional) |

### Release Checklist

1. Update version in all 3 files
2. Update CHANGELOG.md
3. Create PR and merge to main
4. Create GitHub Release with tag `vX.Y.Z`
5. CI automatically publishes to PyPI and GitHub

### Health Checks

```bash
# Verify installation
pip show vlaamscodex

# Check codec registration
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"

# Verify CLI
plats version

# Run test suite
pytest tests/ -v
```

---

## Architecture Quick View

```
vlaamscodex
├── src/vlaamscodex/          # Python package
│   ├── cli.py                # CLI entry point
│   ├── compiler.py           # Transpiler
│   ├── codec.py              # Magic mode codec
│   └── dialects/             # Dialect transformer
├── dialects/                 # 80+ dialect packs (JSON)
├── vscode-extension/         # VS Code extension
├── tests/                    # Test suite
└── .github/workflows/        # CI/CD
```

## Support Channels

- **Issues**: [GitHub Issues](https://github.com/anubissbe/Vlaamse-Codex/issues)
- **Discussions**: GitHub Discussions (if enabled)
- **Maintainer**: See `pyproject.toml` for contact
