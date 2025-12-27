# 📖 Documentation — How Plats works (English, Vlaams style)

Plats (VlaamsCodex) is a tiny parody language.
You tell the computer what to do,
like you’re talking to a person.

No fancy jargon.
No fluff.
Just clear commands.

---

## 🧱 1) How a program starts

Every `.plats` file starts like this:

```text
# coding: vlaamsplats
plan doe
  ...
gedaan
```

- `plan doe` = “start the program”
- `gedaan` = “we’re done”
- Everything in between runs.

That first line (`# coding: vlaamsplats`) is **required** for “magic mode” (see below).

---

## 🧺 2) Remembering things (variables)

To store something:

```text
zet naam op tekst weeireld amen
```

- `zet` = set / store
- `naam` = the variable name
- `op` = “equals”
- `tekst weeireld` = a string
- `amen` = end of the sentence

**Rule:** statements end with `amen`. Forget it and it’s trouble.

---

## 🗣️ 3) Saying something (print)

To print:

```text
klap tekst gdag amen
```

To glue text together (string concat):

```text
klap tekst gdag plakt spatie plakt tekst aan plakt spatie plakt da naam amen
```

- `klap` prints
- `plakt` means “concatenate” (Python `+`)
- `spatie` is exactly one space (`" "`)
- `da naam` reads the variable `naam`

---

## 🧰 4) Functions (reusable pieces)

Define a function:

```text
maak funksie groet met wie doe
  klap tekst gdag plakt spatie plakt da wie amen
gedaan
```

Call a function:

```text
roep groet met da naam amen
```

Return a value:

```text
geeftterug tekst klaar amen
```

---

## 🧠 5) Expressions you can use (v0.1)

- `tekst <words...>` → a string (words joined with spaces)
  - Example: `tekst goeiedag wereld`
- `getal <digits>` → a number
  - Example: `getal 123`
- `da <name>` → variable reference
  - Example: `da naam`
- `spatie` → `" "`
- `plakt` → concatenate (`+`)

For the canonical spec, see `docs/04_language_spec.md`.

---

## ✅ 6) Install

### Option A: pipx (recommended for a CLI tool)

```bash
python -m pip install --user pipx
python -m pipx ensurepath
pipx install vlaamscodex
```

### Option B: venv + pip

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install vlaamscodex
```

### Option C: from source (editable)

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

---

## 🏃 7) Run your `.plats` program

### Option A: CLI (always works)

Run:

```bash
plats run path/to/script.plats
```

Show the generated Python:

```bash
plats show-python path/to/script.plats
```

Compile to a `.py` file:

```bash
plats build path/to/script.plats --out script.py
```

### Option B: Magic mode (`python script.plats`)

If the file starts with:

```text
# coding: vlaamsplats
```

…then this works after install:

```bash
python path/to/script.plats
```

---

## 👋 8) Example: hello world

`examples/hello.plats`:

```text
# coding: vlaamsplats
plan doe
  zet naam op tekst weeireld amen

  maak funksie groet met wie doe
    klap tekst gdag plakt spatie plakt tekst aan plakt spatie plakt da wie amen
  gedaan

  roep groet met da naam amen
gedaan
```

Expected output:

```text
gdag aan weeireld
```

---

## 🪄 9) How the “magic” works (step by step)

This is the whole trick that makes `python script.plats` possible:

1. Python looks at the first two lines of the file to detect an encoding (PEP 263).
2. Your `.plats` file says: `# coding: vlaamsplats`.
3. When Python starts normally, it runs the `site` module.
4. `site` executes `.pth` files inside site-packages.
5. VlaamsCodex installs `data/vlaamscodex_autoload.pth` into site-packages, containing:
   `import vlaamscodex.codec as _vc; _vc.register()`
6. That registers the codec named `vlaamsplats`.
7. When Python opens the `.plats` file, it uses the codec to decode bytes → **Python source text**.
8. Python executes that generated Python source.

So: you write Plats, Python *thinks* it read Python.

---

## 🧯 10) Limitations & troubleshooting

### The big limitation

- `python -S` disables `site` → `.pth` hooks won’t run → magic mode can fail.
- `python -I` (isolated mode) can also block site/user-site → magic mode can fail.

**Fallback that always works:**

```bash
plats run script.plats
```

### Common errors

If you see:

- `python: can't open file ... No such file or directory`
  - Your path is wrong. Use the correct file path.

- `SyntaxError: encoding problem: vlaamsplats`
  - The codec was not registered.
  - Fix: install `vlaamscodex` into the same environment, and don’t run with `-S`/`-I`.

---

## 🔐 11) Security note

`.plats` is code.
Treat it like running a `.py` file:
don’t auto-run untrusted scripts.

