# Troubleshooting

> Solutions for common issues 🔧

Having trouble? This guide covers the most common problems and their solutions.

---

## Quick Fixes Checklist

Before diving into specific issues, try these quick fixes:

| Problem | Quick Fix |
|---------|-----------|
| Command not found | `pip install --upgrade vlaamscodex` |
| Magic mode broken | Check `# coding: vlaamsplats` header |
| Syntax error | Verify all statements end with `amen` |
| Variable undefined | Use `da <name>` to reference variables |
| Block not closed | Add `gedaan` to close the block |

---

## Installation Issues

### "plats: command not found"

**Cause:** The `plats` command is not in your PATH.

**Solutions:**

1. **Add Python scripts to PATH:**

```bash
# Linux/macOS
export PATH="$(python -c 'import site; print(site.USER_BASE)')/bin:$PATH"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export PATH="$(python -c "import site; print(site.USER_BASE)")/bin:$PATH"' >> ~/.bashrc
```

2. **Use the module directly:**

```bash
python -m vlaamscodex run script.plats
```

3. **Reinstall with pip:**

```bash
pip install --force-reinstall vlaamscodex
```

### "No module named 'vlaamscodex'"

**Cause:** VlaamsCodex is not installed in your Python environment.

**Solutions:**

1. **Install the package:**

```bash
pip install vlaamscodex
```

2. **Check you're using the right Python:**

```bash
which python
python -c "import vlaamscodex; print(vlaamscodex.__version__)"
```

3. **If using virtual environments:**

```bash
# Make sure the venv is activated
source venv/bin/activate
pip install vlaamscodex
```

### pip install fails

**Cause:** Python version too old or pip issues.

**Solutions:**

1. **Check Python version (3.10+ required):**

```bash
python --version
```

2. **Upgrade pip:**

```bash
pip install --upgrade pip
```

3. **Install from source:**

```bash
git clone https://github.com/brentishere41848/Vlaams-Codex.git
cd Vlaams-Codex
pip install -e .
```

---

## Magic Mode Issues

### "SyntaxError: encoding problem: vlaamsplats"

**Cause:** The VlaamsCodex codec is not registered.

**Solutions:**

1. **Reinstall VlaamsCodex:**

```bash
pip install --force-reinstall vlaamscodex
```

2. **Verify codec registration:**

```bash
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
```

3. **Check the .pth file exists:**

```bash
python -c "import site; print(site.getsitepackages())"
# Look for vlaamscodex_autoload.pth in those directories
```

4. **Use CLI fallback:**

```bash
plats run script.plats  # Works even if magic mode doesn't
```

### Magic mode works but `python -S` doesn't

**Expected behavior!** The `-S` flag disables the site module, which prevents the codec from loading. Use `plats run` instead.

### File runs with `plats run` but not `python`

**Cause:** Missing or incorrect encoding header.

**Solution:** Make sure your file starts with:

```platskript
# coding: vlaamsplats
plan doe
  ...
gedaan
```

The header must be on line 1 or line 2 (after a shebang).

---

## Syntax Errors

### "Statement must end with 'amen'"

**Cause:** Missing statement terminator.

**Fix:**

```platskript
# ❌ Wrong
klap tekst hello

# ✅ Correct
klap tekst hello amen
```

### "Unclosed block - missing 'gedaan'"

**Cause:** Block started with `doe` but not closed.

**Fix:**

```platskript
# ❌ Wrong
plan doe
  klap tekst hello amen
# Missing gedaan!

# ✅ Correct
plan doe
  klap tekst hello amen
gedaan
```

### "Unknown instruction"

**Cause:** Unrecognized keyword or typo.

**Common issues:**
- `print` instead of `klap`
- `var` instead of `zet ... op`
- `function` instead of `maak funksie`

**Fix:** Use Platskript keywords:

| Python | Platskript |
|--------|------------|
| `print` | `klap` |
| `x = 5` | `zet x op getal 5 amen` |
| `def f():` | `maak funksie f doe` |

### "Variable not defined"

**Cause:** Using a variable without `da`.

**Fix:**

```platskript
# ❌ Wrong - "naam" is treated as literal text
zet naam op tekst Claude amen
klap naam amen

# ✅ Correct - use "da" to reference variables
zet naam op tekst Claude amen
klap da naam amen
```

### "Missing 'doe' after function definition"

**Cause:** Function definition syntax incomplete.

**Fix:**

```platskript
# ❌ Wrong
maak funksie test met x
  klap da x amen
gedaan

# ✅ Correct
maak funksie test met x doe
  klap da x amen
gedaan
```

---

## CLI Issues

### "Unrecognized arguments"

**Cause:** Wrong command syntax or options.

**Solution:** Check help for the specific command:

```bash
plats help
plats examples --help
```

### REPL doesn't start

**Possible causes:**

1. **Terminal issues:**

```bash
# Try with explicit terminal
python -c "from vlaamscodex.repl import run_repl; run_repl()"
```

2. **Environment variables:** Some environments may interfere. Try:

```bash
env -i PATH="$PATH" plats repl
```

### Commands show wrong dialect

**Cause:** Using a dialect alias changes error message language.

**Solution:** Use standard commands for English messages:

```bash
plats check script.plats      # English errors
plats istdagoe script.plats   # Antwerps errors
```

---

## Dialect Issues

### "Could not find dialects directory"

**Cause:** Dialect pack files not found.

**Solutions:**

1. **Reinstall:**

```bash
pip install --force-reinstall vlaamscodex
```

2. **Set custom path:**

```bash
export VLAAMSCODEX_DIALECTS_DIR=/path/to/dialects
```

### "Unknown dialect: xyz"

**Cause:** Specified dialect pack doesn't exist.

**Solution:** List available dialects:

```bash
plats dialecten
```

### Transformation produces unexpected results

**Possible causes:**

1. **Protected terms:** Some words are never transformed (legal/modality terms)

2. **Deterministic mode:** For reproducible results:

```bash
export VLAAMSCODEX_DIALECT_DETERMINISTIC=true
export VLAAMSCODEX_DIALECT_SEED=42
```

3. **Inheritance:** Child dialects inherit from parents. Check pack hierarchy:

```bash
plats dialecten  # Shows inheritance structure
```

---

## VS Code Extension Issues

### Syntax highlighting not working

**Causes and fixes:**

1. **File extension:** Make sure file ends in `.plats`

2. **Language mode:** Click language indicator in status bar, select "Platskript"

3. **Extension not installed:**
   - Open Extensions (`Ctrl+Shift+X`)
   - Search "VlaamsCodex"
   - Install

4. **Reload window:** `Ctrl+Shift+P` → "Developer: Reload Window"

### Snippets not appearing

**Fix:**

1. Make sure you're in a `.plats` file
2. Type snippet prefix (e.g., `plan`)
3. Press `Ctrl+Space` to trigger suggestions

### Commands fail silently

**Cause:** `plats` CLI not found by extension.

**Fix:** Configure the path:

1. Open Settings (`Ctrl+,`)
2. Search "vlaamscodex"
3. Set `Vlaamscodex: Plats Path` to full path of `plats` executable

---

## Build Issues

### pip install -e . fails

**Cause:** Missing build dependencies.

**Solution:**

```bash
pip install build wheel
pip install -e ".[dev]"
```

### Wheel missing .pth file

**Cause:** Build didn't use custom backend.

**Solution:** Build with the project's backend:

```bash
python -m build
```

The custom backend (`vlaamscodex_build_backend.py`) injects the `.pth` file.

### Tests fail

**Steps:**

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_compiler.py -v
```

---

## Getting More Help

### Collect Debug Information

When reporting issues, include:

```bash
# Version info
plats version
python --version
pip show vlaamscodex

# System info
uname -a  # Linux/macOS
# or
systeminfo | findstr /B /C:"OS"  # Windows

# Codec status
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
```

### Where to Get Help

1. **Check existing issues:** [GitHub Issues](https://github.com/brentishere41848/Vlaams-Codex/issues)

2. **Open a new issue:** Include:
   - What you tried
   - What happened
   - What you expected
   - Debug information (above)

3. **Read the docs:**
   - [[Language Reference]] for syntax
   - [[CLI Reference]] for commands
   - [[Getting Started]] for setup

---

## Error Message Reference

### Platskript Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `'amen' vergeten` | Missing statement terminator | Add `amen` |
| `'gedaan' vergeten` | Unclosed block | Add `gedaan` |
| `Onbekende instructie` | Unknown keyword | Check spelling |
| `Variable niet gedefinieerd` | Undefined variable | Define with `zet ... op` |

### Dialect Error Variants

| Region | "Missing amen" Message |
|--------|------------------------|
| West-Vlaams | "Jansen, ge zijt 'amen' vergeten!" |
| Antwerps | "Manneke, gij zijt 'amen' vergeten!" |
| Limburgs | "Jansen, gae zeet 'amen' vergeate!" |
| Brussels | "Allez, ge zijt 'amen' vergeten!" |

---

## See Also

- [[Getting Started]] - Verify your installation
- [[Language Reference]] - Correct syntax
- [[CLI Reference]] - Command usage
- [[Contributing]] - Report issues

---

**Veel succes!** 🧇
