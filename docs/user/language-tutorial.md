# Platskript Language Tutorial

> Learn to write Platskript programs step-by-step.

## What is Platskript?

Platskript is a fun programming language that uses **Flemish dialect keywords**. It compiles to Python and runs anywhere Python runs. Think of it as Python with a Flemish accent!

---

## Lesson 1: Your First Program

Every Platskript program has this structure:

```platskript
# coding: vlaamsplats
plan doe
  <your code here>
gedaan
```

- `# coding: vlaamsplats` - Tells Python to use our codec
- `plan doe` - "Plan, do" = start the program
- `gedaan` - "Done" = end the program

### Hello World

```platskript
# coding: vlaamsplats
plan doe
  klap tekst gdag weeireld amen
gedaan
```

- `klap` - Print (literally "clap" or "say")
- `tekst gdag weeireld` - The string "gdag weeireld"
- `amen` - Statement terminator (like `;` in other languages)

**Output:** `gdag weeireld`

### The Golden Rule

**Every statement must end with `amen`!**

```platskript
# Correct
klap tekst hello amen

# Wrong - will fail!
klap tekst hello
```

---

## Lesson 2: Variables

Store values in variables with `zet ... op`:

```platskript
# coding: vlaamsplats
plan doe
  zet naam op tekst Vlaanderen amen
  klap da naam amen
gedaan
```

- `zet naam op` - "Set name to"
- `tekst Vlaanderen` - The string "Vlaanderen"
- `da naam` - "The name" = reference variable `naam`

**Output:** `Vlaanderen`

### Multiple Words in Strings

```platskript
zet boodschap op tekst goedemorgen iedereen amen
klap da boodschap amen
```

**Output:** `goedemorgen iedereen`

---

## Lesson 3: Numbers and Math

### Number Literals

```platskript
zet x op getal 42 amen
klap da x amen
```

**Output:** `42`

### Math Operators

| Platskript | Python | Description |
|------------|--------|-------------|
| `derbij` | `+` | Addition |
| `deraf` | `-` | Subtraction |
| `keer` | `*` | Multiplication |
| `gedeeld` | `/` | Division |

### Example: Calculator

```platskript
# coding: vlaamsplats
plan doe
  zet x op getal 10 amen
  zet y op getal 5 amen

  zet som op da x derbij da y amen
  klap da som amen

  zet verschil op da x deraf da y amen
  klap da verschil amen

  zet product op da x keer da y amen
  klap da product amen
gedaan
```

**Output:**
```
15
5
50
```

---

## Lesson 4: String Concatenation

Use `plakt` to join strings together:

```platskript
klap tekst hallo plakt spatie plakt tekst wereld amen
```

- `plakt` - "Sticks" = concatenation (`+` in Python)
- `spatie` - Space character `" "`

**Output:** `hallo wereld`

### Building Complex Strings

```platskript
# coding: vlaamsplats
plan doe
  zet naam op tekst Claude amen
  zet groet op tekst gdag aan amen

  klap da groet plakt spatie plakt da naam amen
gedaan
```

**Output:** `gdag aan Claude`

---

## Lesson 5: Functions

### Defining Functions

```platskript
maak funksie <name> met <params> doe
  <statements>
gedaan
```

### Example: Greeting Function

```platskript
# coding: vlaamsplats
plan doe
  maak funksie groet met wie doe
    klap tekst hallo plakt spatie plakt da wie amen
  gedaan

  roep groet met tekst wereld amen
gedaan
```

- `maak funksie groet met wie doe` - "Make function greet with who do"
- `roep groet met tekst wereld amen` - "Call greet with 'wereld'"

**Output:** `hallo wereld`

### Multiple Parameters

```platskript
# coding: vlaamsplats
plan doe
  maak funksie zeghet met wat en aan doe
    klap da wat plakt spatie plakt da aan amen
  gedaan

  roep zeghet met tekst gdag en tekst vriend amen
gedaan
```

**Output:** `gdag vriend`

### Return Values

```platskript
# coding: vlaamsplats
plan doe
  maak funksie telop met a en b doe
    geeftterug da a derbij da b amen
  gedaan

  zet resultaat op roep telop met getal 5 en getal 3 amen
  klap da resultaat amen
gedaan
```

- `geeftterug` - "Give back" = return

**Output:** `8`

---

## Lesson 6: Complete Example

Let's put it all together:

```platskript
# coding: vlaamsplats
plan doe
  zet naam op tekst weeireld amen

  maak funksie groet met wie doe
    klap tekst gdag plakt spatie plakt tekst aan plakt spatie plakt da wie amen
  gedaan

  maak funksie bereken met x en y doe
    zet som op da x derbij da y amen
    klap tekst som is plakt spatie plakt da som amen
    geeftterug da som amen
  gedaan

  roep groet met da naam amen
  roep bereken met getal 10 en getal 5 amen
gedaan
```

**Output:**
```
gdag aan weeireld
som is 15
```

---

## Language Reference

### Program Structure

```platskript
# coding: vlaamsplats
plan doe
  <statements>
gedaan
```

### Statements

| Statement | Syntax | Description |
|-----------|--------|-------------|
| Print | `klap <expr> amen` | Print expression |
| Assignment | `zet <var> op <expr> amen` | Assign to variable |
| Function def | `maak funksie <name> met <params> doe ... gedaan` | Define function |
| Function call | `roep <name> met <args> amen` | Call function |
| Return | `geeftterug <expr> amen` | Return value |

### Expressions

| Expression | Syntax | Description |
|------------|--------|-------------|
| String | `tekst hello world` | String literal |
| Number | `getal 42` | Number literal |
| Variable | `da <name>` | Variable reference |
| Space | `spatie` | Space character |
| Concat | `<expr> plakt <expr>` | String concatenation |

### Operators

| Operator | Platskript | Description |
|----------|------------|-------------|
| Add | `derbij` | Addition |
| Subtract | `deraf` | Subtraction |
| Multiply | `keer` | Multiplication |
| Divide | `gedeeld` | Division |
| Equals | `isgelijk` | Equality |
| Not equals | `isniegelijk` | Inequality |
| Greater | `isgroterdan` | Greater than |
| Less | `iskleinerdan` | Less than |
| And | `enook` | Logical AND |
| Or | `ofwel` | Logical OR |
| Not | `nie` | Logical NOT |

---

## Common Mistakes

### 1. Forgetting `amen`

```platskript
# Wrong
klap tekst hello

# Correct
klap tekst hello amen
```

### 2. Forgetting `da` for Variables

```platskript
# Wrong
klap naam amen

# Correct
klap da naam amen
```

### 3. Forgetting `gedaan` to Close Blocks

```platskript
# Wrong
plan doe
  klap tekst hello amen
# Missing gedaan!

# Correct
plan doe
  klap tekst hello amen
gedaan
```

### 4. Missing `doe` After Function Definition

```platskript
# Wrong
maak funksie test met x
  klap da x amen
gedaan

# Correct
maak funksie test met x doe
  klap da x amen
gedaan
```

---

## Practice Exercises

### Exercise 1: Personal Greeting

Write a program that:
1. Stores your name in a variable
2. Prints "Gdag [your name]!"

### Exercise 2: Simple Calculator

Write a program that:
1. Stores two numbers
2. Calculates and prints their sum, difference, and product

### Exercise 3: Greeting Function

Write a function that:
1. Takes a name and a greeting as parameters
2. Prints them together with proper spacing

---

## What's Next?

- **[CLI Reference](cli-reference.md)**: All commands and options
- **[Dialect Guide](dialect-guide.md)**: Transform text to regional dialects
- **[Examples](../examples/)**: More example programs

---

**Veel plansen!** 🧇
