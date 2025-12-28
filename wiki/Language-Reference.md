# Language Reference

> Complete Platskript v0.1 language specification 📖

This is the authoritative reference for the Platskript programming language syntax and semantics.

---

## File Structure

Every Platskript program has this structure:

```platskript
# coding: vlaamsplats
plan doe
  <statements>
gedaan
```

| Element | Required | Purpose |
|---------|----------|---------|
| `# coding: vlaamsplats` | For magic mode | Enables `python file.plats` execution |
| `plan doe ... gedaan` | Yes | Program entry point and main block |

### Notes

- **Whitespace**: Indentation is for readability only; it's not semantically significant
- **Blocks**: Delimited by keywords (`doe` ... `gedaan`), not indentation
- **Encoding**: Files should be UTF-8

---

## Statement Terminator

**Every statement must end with `amen`!**

This is the Platskript equivalent of `;` in other languages.

```platskript
# ✅ Correct
klap tekst hello amen

# ❌ Wrong - will cause an error
klap tekst hello
```

---

## Statements

### Print Statement

Output an expression to the console.

```platskript
klap <expression> amen
```

**Examples:**

```platskript
klap tekst Hello World amen     # Print string
klap getal 42 amen              # Print number
klap da variabele amen          # Print variable
klap da x derbij da y amen      # Print expression result
```

### Variable Assignment

Store a value in a variable.

```platskript
zet <name> op <expression> amen
```

**Examples:**

```platskript
zet x op getal 10 amen                          # Number
zet naam op tekst Claude amen                   # String
zet resultaat op da a plakt da b amen           # Expression
zet som op da x derbij da y amen                # Arithmetic
```

### Return Statement

Return a value from a function.

```platskript
geeftterug <expression> amen
```

**Example:**

```platskript
maak funksie dubbel met n doe
  geeftterug da n keer getal 2 amen
gedaan
```

---

## Expressions

### Literals

| Type | Syntax | Example | Python Equivalent |
|------|--------|---------|-------------------|
| String | `tekst <words>` | `tekst hello world` | `"hello world"` |
| Number | `getal <n>` | `getal 42` | `42` |
| Space | `spatie` | `spatie` | `" "` |

**String Notes:**
- `tekst` captures all following words until an operator or statement boundary
- Multi-word strings work automatically: `tekst hello world` → `"hello world"`

### Variable Reference

Access a variable's value using `da` ("the"):

```platskript
da <name>
```

**Example:**

```platskript
zet x op getal 5 amen
klap da x amen          # Prints: 5
```

⚠️ **Important:** You must use `da` to reference variables. Without it, the word is treated as literal text.

### Operators

#### Arithmetic Operators

| Platskript | Python | Description |
|------------|--------|-------------|
| `derbij` | `+` | Addition |
| `deraf` | `-` | Subtraction |
| `keer` | `*` | Multiplication |
| `gedeeld` | `/` | Division |
| `rest` | `%` | Modulo (remainder) |
| `tot` | `**` | Power/Exponentiation |

**Alternative forms:** `plus`, `min`, `maal`, `gedeelddoor`, `door`

**Example:**

```platskript
zet som op getal 5 derbij getal 3 amen        # 8
zet verschil op getal 10 deraf getal 4 amen   # 6
zet product op getal 6 keer getal 7 amen      # 42
zet quotient op getal 20 gedeeld getal 4 amen # 5.0
```

#### String Concatenation

| Platskript | Python | Description |
|------------|--------|-------------|
| `plakt` | `+` | String concatenation |

**Example:**

```platskript
zet groet op tekst Hallo plakt spatie plakt tekst wereld amen
klap da groet amen      # Prints: Hallo wereld
```

#### Comparison Operators

| Platskript | Python | Description |
|------------|--------|-------------|
| `isgelijk` / `izz` | `==` | Equal to |
| `isniegelijk` / `izzniet` | `!=` | Not equal to |
| `isgroterdan` / `groterdan` | `>` | Greater than |
| `iskleinerdan` / `kleinerdan` | `<` | Less than |
| `groterofgelijk` | `>=` | Greater or equal |
| `kleinerofgelijk` | `<=` | Less or equal |

#### Logical Operators

| Platskript | Python | Description |
|------------|--------|-------------|
| `enook` / `en` | `and` | Logical AND |
| `ofwel` / `of` | `or` | Logical OR |
| `nie` / `niet` | `not` | Logical NOT |

---

## Control Flow

### Conditional (If/Else)

```platskript
als <condition> dan doe
  <statements>
gedaan
```

With else branch:

```platskript
als <condition> dan doe
  <statements>
anders doe
  <statements>
gedaan
```

**Example:**

```platskript
zet x op getal 10 amen
als da x groterdan getal 5 dan doe
  klap tekst Groot! amen
anders doe
  klap tekst Klein! amen
gedaan
```

### While Loop

```platskript
zolang <condition> doe
  <statements>
gedaan
```

**Example:**

```platskript
zet i op getal 0 amen
zolang da i kleinerdan getal 5 doe
  klap da i amen
  zet i op da i derbij getal 1 amen
gedaan
```

### For Loop

```platskript
voor <var> in <iterable> doe
  <statements>
gedaan
```

**Example:**

```platskript
voor item in da lijst doe
  klap da item amen
gedaan
```

---

## Functions

### Function Definition

Without parameters:

```platskript
maak funksie <name> doe
  <statements>
gedaan
```

With one parameter:

```platskript
maak funksie <name> met <param> doe
  <statements>
gedaan
```

With multiple parameters (use `en` to separate):

```platskript
maak funksie <name> met <param1> en <param2> doe
  <statements>
gedaan
```

### Function Call

Without arguments:

```platskript
roep <name> amen
```

With arguments:

```platskript
roep <name> met <arg1> amen
roep <name> met <arg1> en <arg2> amen
```

### Complete Example

```platskript
# coding: vlaamsplats
plan doe
  maak funksie begroet met naam doe
    klap tekst Hallo plakt spatie plakt da naam plakt tekst ! amen
  gedaan

  maak funksie optellen met a en b doe
    geeftterug da a derbij da b amen
  gedaan

  roep begroet met tekst Claude amen

  zet resultaat op roep optellen met getal 5 en getal 3 amen
  klap da resultaat amen
gedaan
```

**Output:**

```
Hallo Claude!
8
```

---

## Block Structure

All blocks use `doe ... gedaan`:

| Block Type | Syntax |
|------------|--------|
| Main program | `plan doe ... gedaan` |
| Function | `maak funksie <name> [met <params>] doe ... gedaan` |
| If | `als <condition> dan doe ... gedaan` |
| Else | `anders doe ... gedaan` |
| While | `zolang <condition> doe ... gedaan` |
| For | `voor <var> in <iter> doe ... gedaan` |

---

## Comments

```platskript
# This is a comment
klap tekst hello amen  # Inline comment
```

Comments start with `#` and continue to end of line.

---

## Keywords Summary

| Category | Keywords |
|----------|----------|
| **Structure** | `plan`, `doe`, `gedaan`, `amen` |
| **Variables** | `zet`, `op`, `da` |
| **Output** | `klap` |
| **Functions** | `maak`, `funksie`, `met`, `en`, `roep`, `geeftterug` |
| **Control Flow** | `als`, `dan`, `anders`, `zolang`, `voor`, `in` |
| **Literals** | `tekst`, `getal`, `spatie` |
| **Arithmetic** | `derbij`, `deraf`, `keer`, `gedeeld`, `rest`, `tot`, `plakt` |
| **Comparison** | `isgelijk`, `isniegelijk`, `isgroterdan`, `iskleinerdan` |
| **Logical** | `enook`, `ofwel`, `nie` |

---

## Complete Program Example

```platskript
# coding: vlaamsplats
# A simple calculator program

plan doe
  # Define addition function
  maak funksie optellen met a en b doe
    geeftterug da a derbij da b amen
  gedaan

  # Define multiplication function
  maak funksie vermenigvuldig met a en b doe
    geeftterug da a keer da b amen
  gedaan

  # Use the functions
  zet x op getal 10 amen
  zet y op getal 5 amen

  klap tekst Som: amen
  zet som op roep optellen met da x en da y amen
  klap da som amen

  klap tekst Product: amen
  zet prod op roep vermenigvuldig met da x en da y amen
  klap da prod amen

  # Conditional logic
  als da som groterdan da prod dan doe
    klap tekst Som is groter amen
  anders doe
    klap tekst Product is groter of gelijk amen
  gedaan
gedaan
```

---

## See Also

- [[Language Tutorial]] - Step-by-step learning
- [[Getting Started]] - Installation and first steps
- [[CLI Reference]] - Command line tools
- [[Examples Gallery]] - Sample programs

---

**Veel plansen!** 🧇
