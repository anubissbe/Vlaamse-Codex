# Magic Mode

> How `python script.plats` works 🪄

Magic Mode allows you to execute Platskript files directly with Python, just like regular Python scripts. This page explains the mechanism behind it.

---

## What is Magic Mode?

Magic Mode lets you run Platskript files directly:

```bash
python myscript.plats
```

Instead of requiring:

```bash
plats run myscript.plats
```

---

## How It Works

### Key Insight: Python Decodes Before Parsing

When you run `python myscript.plats`, Python:

1. **Read bytes** from the file
2. **Decode** those bytes into text using an encoding
3. **Parse** the resulting text as Python syntax
4. **Execute** the compiled code object

If we intercept step 2 and return *different text* (valid Python), then Python happily parses and executes it.

### The Encoding Cookie

Python supports declaring a source encoding in the first or second line of a file (PEP 263):

```python
# coding: utf-8
```

The encoding name can be **any encoding** that Python can resolve through its codec registry.

So if the first line is:

```platskript
# coding: vlaamsplats
```

Python will try to locate a codec named `vlaamsplats`. If it exists, Python uses it to decode the file.

---

## The Codec Registry

Python can be taught new encodings at runtime:

1. Implement a codec (a `codecs.CodecInfo` with encode/decode functions)
2. Register a search function via `codecs.register(search_function)`
3. When Python sees an encoding name, it calls registered search functions

### What Our Decoder Does

For the `vlaamsplats` codec, the decoder:

1. Decodes bytes as UTF-8 (getting original Plats text)
2. Removes the `# coding: vlaamsplats` line
3. Compiles/translates Plats source into valid Python
4. Returns that Python string as the "decoded text"

From Python's perspective, it just decoded the file. It doesn't know (or care) that it was a transformation.

---

## Implementation

### Codec Class (`codec.py`)

```python
import codecs
from vlaamscodex.compiler import compile_plats

class VlaamsPlatsCodec(codecs.Codec):
    def decode(self, input_bytes, errors='strict'):
        # 1. Decode bytes as UTF-8 to get Plats source
        plats_src = input_bytes.decode('utf-8')

        # 2. Compile to Python
        python_src = compile_plats(plats_src)

        # 3. Return Python source (as if we "decoded" it)
        return python_src, len(input_bytes)

    def encode(self, input_string, errors='strict'):
        # Encoding is rarely needed, just pass through
        return input_string.encode('utf-8'), len(input_string)
```

### Registration

```python
def search_function(encoding_name):
    if encoding_name == 'vlaamsplats':
        return codecs.CodecInfo(
            name='vlaamsplats',
            encode=VlaamsPlatsCodec().encode,
            decode=VlaamsPlatsCodec().decode,
            incrementalencoder=codecs.IncrementalEncoder,
            incrementaldecoder=codecs.IncrementalDecoder,
        )
    return None

def register():
    codecs.register(search_function)
```

---

## The Startup Hook

### The Hard Requirement

The codec must be registered **BEFORE** Python reads the file. Python needs the codec while decoding the script file itself.

### The `.pth` Solution

Python's `site` module processes `.pth` files in site-packages at startup. A `.pth` file may contain an `import ...` line which gets executed.

**`data/vlaamscodex_autoload.pth`:**

```python
import vlaamscodex.codec; vlaamscodex.codec.register()
```

When this `.pth` file is in site-packages, Python:
1. Starts up
2. Processes site initialization
3. Sees our `.pth` file
4. Executes the import line
5. Our codec is registered

This happens **before** the main script is loaded, so the codec is ready.

### Alternative Approaches

| Approach | Pros | Cons |
|----------|------|------|
| **`.pth` hook** (used) | Automatic, invisible | Requires site initialization |
| `sitecustomize.py` | Standard Python | May conflict with others |
| Explicit runner | Most robust | Requires `plats run` |

---

## Build Integration

### Custom Build Backend

The `.pth` file must end up in `site-packages` root. This requires special build handling.

**`vlaamscodex_build_backend.py`** is a custom PEP 517 build backend that:

1. Wraps `setuptools.build_meta`
2. Injects `vlaamscodex_autoload.pth` into the wheel's data directory
3. Ensures the `.pth` file lands in `site-packages` upon installation

```python
def build_wheel(wheel_directory, config_settings, metadata_directory):
    # 1. Build wheel normally with setuptools
    filename = _orig.build_wheel(wheel_directory, config_settings, metadata_directory)

    # 2. Post-process: inject .pth
    _ensure_autoload_pth_in_wheel(Path(wheel_directory) / filename)

    return filename
```

**See:** [[Build-and-Release]] for complete build system documentation.

---

## Using Magic Mode

### Creating a Magic Mode File

Your `.plats` file must have the encoding cookie on line 1 or 2:

```platskript
# coding: vlaamsplats
plan doe
  klap tekst Hallo weeireld! amen
gedaan
```

Or after a shebang:

```platskript
#!/usr/bin/env python
# coding: vlaamsplats
plan doe
  klap tekst Hallo weeireld! amen
gedaan
```

### Running

```bash
python myscript.plats
```

Output:
```
Hallo weeireld!
```

---

## Limitations

### When Magic Mode Fails

| Flag | Issue |
|------|-------|
| `python -S` | Disables site initialization |
| `python -I` | Isolated mode, restricted site-packages |
| Embedded Python | May not process `.pth` hooks |

### Workaround

Use the explicit runner:

```bash
plats run myscript.plats  # Always works
```

### Error Reporting

Since the transpiler operates before Python's parser:

- Line numbers in tracebacks refer to **generated Python**
- Error messages are Python errors, not Platskript-native

**Future improvement**: Implement source maps for Plats → Python line mapping.

---

## Verification

### Check Codec Registration

```bash
python -c "import codecs; print(codecs.lookup('vlaamsplats'))"
```

Should output:
```
<codecs.CodecInfo object for encoding vlaamsplats at 0x...>
```

### Check `.pth` File

```bash
ls $(python -c "import site; print(site.getsitepackages()[0])")/*.pth
```

Should include `vlaamscodex_autoload.pth`.

### Test Magic Mode

```bash
echo '# coding: vlaamsplats
plan doe
  klap tekst test amen
gedaan' > /tmp/test.plats

python /tmp/test.plats
```

Should output: `test`

---

## Troubleshooting

### "SyntaxError: encoding problem: vlaamsplats"

**Cause:** Codec not registered.

**Solutions:**

1. Reinstall VlaamsCodex:
   ```bash
   pip install --force-reinstall vlaamscodex
   ```

2. Verify `.pth` file exists:
   ```bash
   python -c "import site; print(site.getsitepackages())"
   # Look for vlaamscodex_autoload.pth in those directories
   ```

3. Use CLI fallback:
   ```bash
   plats run script.plats  # Works even if magic mode doesn't
   ```

### Magic Mode Works but `python -S` Doesn't

**Expected behavior!** The `-S` flag disables the site module, which prevents the codec from loading.

### File Runs with `plats run` but Not `python`

**Cause:** Missing or incorrect encoding header.

**Solution:** Ensure your file starts with:

```platskript
# coding: vlaamsplats
```

The header must be on line 1 or line 2 (after a shebang).

---

## Security Note

Executing arbitrary `.plats` means executing generated Python. If `.plats` comes from untrusted users, treat it like untrusted code:

- Run in a sandbox
- Restrict filesystem/network access
- Don't execute automatically from untrusted sources

---

## Files

| File | Purpose |
|------|---------|
| `src/vlaamscodex/codec.py` | Codec implementation |
| `data/vlaamscodex_autoload.pth` | Startup hook |
| `vlaamscodex_build_backend.py` | Build backend for .pth injection |

---

## See Also

- [[Transpiler-Internals]] - How Platskript compiles to Python
- [[Build-and-Release]] - Build system and .pth injection
- [[Troubleshooting]] - Common problems and solutions
- [[Architecture-Overview]] - System design

---

**Veel plansen!** 🧇
