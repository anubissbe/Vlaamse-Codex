# Troubleshooting Guide

> Solutions for common VlaamsCodex issues.

## Installation Issues

### "Command not found: plats"

**Cause:** The `plats` command isn't in your PATH.

**Solutions:**

1. **Verify installation:**
   ```bash
   pip show vlaamscodex
   ```

2. **Check if scripts directory is in PATH:**
   ```bash
   python -c "import site; print(site.USER_BASE + '/bin')"
   ```

   Add this to your shell's PATH if missing.

3. **Use module directly:**
   ```bash
   python -m vlaamscodex run script.plats
   ```

4. **Reinstall with pipx:**
   ```bash
   pipx install vlaamscodex
   ```

---

### "No module named 'vlaamscodex'"

**Cause:** Package not installed in your Python environment.

**Solutions:**

1. **Install the package:**
   ```bash
   pip install vlaamscodex
   ```

2. **Check you're using the right Python:**
   ```bash
   which python
   python -m pip list | grep vlaams
   ```

3. **If using virtual environment, activate it first:**
   ```bash
   source .venv/bin/activate
   pip install vlaamscodex
   ```

---

## Magic Mode Issues

### "SyntaxError: encoding problem: vlaamsplats"

**Cause:** The `vlaamsplats` codec isn't registered.

**Solutions:**

1. **Make sure package is installed:**
   ```bash
   pip install vlaamscodex
   ```

2. **Check codec is registered:**
   ```bash
   python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
   ```

3. **Don't use `-S` or `-I` flags:**
   ```bash
   # Wrong - disables site module
   python -S script.plats

   # Correct
   python script.plats
   ```

4. **Fallback to CLI:**
   ```bash
   plats run script.plats
   ```

---

### "python: can't open file ... No such file or directory"

**Cause:** File path is incorrect.

**Solutions:**

1. **Check file exists:**
   ```bash
   ls -la script.plats
   ```

2. **Use full path:**
   ```bash
   python /full/path/to/script.plats
   ```

3. **Check current directory:**
   ```bash
   pwd
   ls *.plats
   ```

---

## Syntax Errors

### "'amen' vergeten" / Missing 'amen'

**Cause:** Statement doesn't end with `amen`.

**Wrong:**
```platskript
klap tekst hello
```

**Correct:**
```platskript
klap tekst hello amen
```

---

### "unclosed blocks"

**Cause:** Missing `gedaan` to close a block.

**Wrong:**
```platskript
plan doe
  klap tekst hello amen
```

**Correct:**
```platskript
plan doe
  klap tekst hello amen
gedaan
```

---

### "unknown instruction"

**Cause:** Unrecognized keyword or syntax.

**Common mistakes:**

| Wrong | Correct |
|-------|---------|
| `print hello` | `klap tekst hello amen` |
| `x = 5` | `zet x op getal 5 amen` |
| `def func():` | `maak funksie func doe` |

**Check:**
- Correct keywords: `klap`, `zet`, `maak funksie`, `roep`, `geeftterug`
- Proper structure: `plan doe ... gedaan`
- Statement terminators: `amen`

---

### Variable not defined

**Cause:** Using a variable before assigning it.

**Wrong:**
```platskript
plan doe
  klap da naam amen
gedaan
```

**Correct:**
```platskript
plan doe
  zet naam op tekst Claude amen
  klap da naam amen
gedaan
```

---

## CLI Issues

### "unrecognized arguments"

**Cause:** Wrong command syntax.

**Check usage:**
```bash
plats help
plats run --help
plats build --help
```

**Common mistakes:**

| Wrong | Correct |
|-------|---------|
| `plats script.plats` | `plats run script.plats` |
| `plats build script.plats output.py` | `plats build script.plats --out output.py` |
| `plats examples hello` | `plats examples --run hello` |

---

### REPL doesn't start

**Cause:** Interactive mode issue.

**Solutions:**

1. **Check terminal supports interactive input:**
   ```bash
   plats repl
   ```

2. **Try different terminal emulator**

3. **Check Python installation:**
   ```bash
   python -c "import readline"
   ```

---

## Dialect Transformation Issues

### "Could not find dialects directory"

**Cause:** Dialect packs not installed properly.

**Solutions:**

1. **Reinstall package:**
   ```bash
   pip uninstall vlaamscodex
   pip install vlaamscodex
   ```

2. **Check dialects location:**
   ```bash
   python -c "import site; print(site.getsitepackages()[0] + '/dialects')"
   ls $(python -c "import site; print(site.getsitepackages()[0])")/dialects/
   ```

3. **Set environment variable:**
   ```bash
   export VLAAMSCODEX_DIALECTS_DIR=/path/to/dialects
   ```

---

### "Unknown dialect: xxx"

**Cause:** Invalid dialect ID.

**Solution:**
```bash
# List valid dialects
plats dialecten
```

**Common dialects:**
- `algemeen-vlaams`
- `antwerps`
- `west-vlaams`
- `limburgs`
- `brussels`

---

## Build Issues

### "pip install -e ." fails

**Solutions:**

1. **Update build tools:**
   ```bash
   pip install --upgrade pip setuptools wheel build
   ```

2. **Install with verbose output:**
   ```bash
   pip install -e . -v
   ```

3. **Check Python version (3.10+ required):**
   ```bash
   python --version
   ```

---

### Wheel doesn't include .pth file

**Cause:** Custom build backend issue.

**Solutions:**

1. **Rebuild cleanly:**
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   ```

2. **Check wheel contents:**
   ```bash
   unzip -l dist/vlaamscodex-*.whl | grep pth
   ```

3. **Verify build backend in pyproject.toml:**
   ```toml
   [build-system]
   build-backend = "vlaamscodex_build_backend"
   ```

---

## VS Code Extension Issues

### Syntax highlighting not working

**Solutions:**

1. **Check file extension is `.plats`**

2. **Reload VS Code:**
   - `Ctrl+Shift+P` → "Reload Window"

3. **Check extension is installed:**
   - Extensions panel → Search "VlaamsCodex"

4. **Set language mode manually:**
   - Click language indicator in status bar
   - Select "Platskript"

---

### Snippets not appearing

**Solutions:**

1. **Trigger suggestions:** `Ctrl+Space`

2. **Check snippets are enabled:**
   - Settings → "Editor: Tab Completion" → "on"

---

## Getting More Help

### Check Version

```bash
plats version
python -c "import vlaamscodex; print(vlaamscodex.__version__)"
```

### Run with Debug Output

```bash
# Show generated Python
plats show-python script.plats

# Validate syntax
plats check script.plats
```

### Report Issues

Open an issue at: https://github.com/anubissbe/Vlaamse-Codex/issues

Include:
- Python version: `python --version`
- VlaamsCodex version: `plats version`
- Operating system
- Full error message
- Minimal code to reproduce

---

## Quick Fixes Checklist

| Problem | Quick Fix |
|---------|-----------|
| Command not found | `pip install vlaamscodex` |
| Magic mode fails | Use `plats run` instead |
| Missing 'amen' | Add `amen` to end of statement |
| Unclosed block | Add `gedaan` |
| Variable error | Use `da variable` syntax |
| Unknown dialect | Run `plats dialecten` |

---

**'t Es simpel, 't es plansen!** 🧇
