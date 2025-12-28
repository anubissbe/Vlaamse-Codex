# Update Architecture Workflow

## Purpose

Maintain architecture documentation to stay current with project evolution. This workflow ensures technical documentation accurately reflects the current state of the codebase.

## When to Run

- After significant structural changes
- When new subsystems are added
- Before major releases
- When onboarding documentation feels stale

## Workflow Steps

### 1. Inventory Current Documentation

Identify all existing architecture and technical documentation:

```bash
# Find architecture docs
ls docs/architecture/

# Find other technical docs
ls docs/*.md

# Check CLAUDE.md
cat CLAUDE.md
```

**Key locations**:
- `docs/architecture/` - System architecture documents
- `docs/` - User-facing documentation
- `CLAUDE.md` - AI assistant guidance
- `dialects/README.md` - Dialect pack documentation
- `dialects/schema.md` - Pack format specification

### 2. Analyze Current Project Structure

Map the actual codebase structure:

```bash
# Python package structure
rg --files src/ -g "*.py"

# Dialect packs
ls dialects/packs/ | wc -l

# Tools
ls tools/

# VS Code extension
ls vscode-extension/src/
```

**Key areas to verify**:
- [ ] `src/vlaamscodex/` modules match documented components
- [ ] `dialects/` structure matches schema documentation
- [ ] `tools/` utilities are documented
- [ ] Build system (`pyproject.toml`, `vlaamscodex_build_backend.py`) is accurate

### 3. Identify Gaps

Compare documented vs. actual:

| Area | Documented? | Current? | Action |
|------|-------------|----------|--------|
| Transpiler pipeline | Yes | Yes | Verify accuracy |
| Dialect transformer | Partial | Yes | Update/expand |
| CLI commands | Yes | Yes | Check new aliases |
| VS Code extension | Brief | Yes | Verify |
| Pack format | Yes | Yes | Check for new rule types |

### 4. Update Documents

Priority order:
1. **CLAUDE.md** - Primary AI guidance (most impactful)
2. **docs/architecture/00_overview.md** - High-level system view
3. **docs/architecture/01_transpiler.md** - Compiler/codec details
4. **docs/architecture/02_dialect_transformer.md** - Transformation engine
5. **docs/architecture/03_cli.md** - Command routing

### 5. Verify Consistency

Cross-check:
- Version numbers match across files
- File paths referenced actually exist
- Command examples work
- Diagrams reflect current flow

### 6. Commit Updates

```bash
git add docs/architecture/ CLAUDE.md
git commit -m "docs: Update architecture documentation"
```

## Document Templates

### New Architecture Document

```markdown
# [Component Name] Architecture

Brief description of what this component does.

## Overview

ASCII diagram showing component relationships.

## Core Components

### [Subcomponent 1]

What it does, key functions, how to use.

### [Subcomponent 2]

...

## Configuration

Environment variables, config files, options.

## Files

| File | Purpose |
|------|---------|
| path/to/file | What it does |

## Extending

How to add new features to this component.
```

## Checklist

Before completing:

- [ ] All architecture docs updated
- [ ] CLAUDE.md reflects current state
- [ ] No dead file references
- [ ] No outdated version numbers
- [ ] Command examples verified
- [ ] New subsystems documented
- [ ] Diagrams updated
