# Language Tutorial

> Learn to write Platskript programs step-by-step! 📚

This tutorial will teach you Platskript from scratch. By the end, you'll be able to write complete programs with variables, functions, and more.

---

## What is Platskript?

Platskript is a fun programming language that uses **Flemish dialect keywords** instead of English. It compiles to Python and runs anywhere Python runs.

Think of it as Python with a Flemish accent! 🧇

| English | Platskript |
|---------|------------|
| `print("hello")` | `klap tekst hello amen` |
| `x = 5` | `zet x op getal 5 amen` |
| `def greet(name):` | `maak funksie greet met name doe` |

---

## Lesson 1: Your First Program

Every Platskript program has this structure:

```platskript
# coding: vlaamsplats
plan doe
  <your code here>
gedaan
```

| Part | Meaning |
|------|---------|
| `# coding: vlaamsplats` | Tells Python to use the VlaamsCodex codec |
| `plan doe` | "Plan, do" - Start the program |
| `gedaan` | "Done" - End the program |

### Hello World

Create `hello.plats`:

```platskript
# coding: vlaamsplats
plan doe
  klap tekst gdag weeireld amen
gedaan
```

Run it:

```bash
python hello.plats
```

**Output:** `gdag weeireld`

### Understanding the Code

| Token | Meaning |
|-------|---------|
| `klap` | "Clap" or "say" = Print |
| `tekst gdag weeireld` | The string "gdag weeireld" |
| `amen` | Statement terminator (like `;` in other languages) |

### ⚠️ The Golden Rule

**Every statement must end with `amen`!**

```platskript
# ✅ Correct
klap tekst hello amen

# ❌ Wrong - will fail!
klap tekst hello
```

---

## Lesson 2: Variables

Store values in variables with `zet ... op` ("set ... to"):

```platskript
# coding: vlaamsplats
plan doe
  zet naam op tekst Vlaanderen amen
  klap da naam amen
gedaan
```

**Output:** `Vlaanderen`

### Key Concepts

| Code | Meaning |
|------|---------|
| `zet naam op` | "Set name to" |
| `tekst Vlaanderen` | String literal "Vlaanderen" |
| `da naam` | "The name" - Reference the variable |

### Multiple Words in Strings

```platskript
zet boodschap op tekst goedemorgen iedereen amen
klap da boodschap amen
```

**Output:** `goedemorgen iedereen`

### ⚠️ Don't Forget `da`!

You must use `da` to reference variables:

```platskript
# ✅ Correct
klap da naam amen

# ❌ Wrong - "naam" won't be recognized as a variable
klap naam amen
```

---

## Lesson 3: Numbers and Math

### Number Literals

Use `getal` ("number") for numeric values:

```platskript
zet x op getal 42 amen
klap da x amen
```

**Output:** `42`

### Math Operators

| Platskript | Python | Description |
|------------|--------|-------------|
| `derbij` | `+` | Addition ("there by") |
| `deraf` | `-` | Subtraction ("there off") |
| `keer` | `*` | Multiplication ("times") |
| `gedeeld` | `/` | Division ("divided") |

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

Use `plakt` ("sticks") to join strings together:

```platskript
klap tekst hallo plakt spatie plakt tekst wereld amen
```

**Output:** `hallo wereld`

### Key Tokens

| Token | Meaning |
|-------|---------|
| `plakt` | "Sticks" = Concatenation (like `+` for strings) |
| `spatie` | Space character `" "` |

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

### Mixing Strings and Variables

```platskript
# coding: vlaamsplats
plan doe
  zet wie op tekst wereld amen
  klap tekst hallo plakt spatie plakt da wie plakt tekst ! amen
gedaan
```

**Output:** `hallo wereld!`

---

## Lesson 5: Functions

### Defining Functions

```platskript
maak funksie <name> met <params> doe
  <statements>
gedaan
```

| Part | Meaning |
|------|---------|
| `maak funksie` | "Make function" |
| `met` | "With" (parameters follow) |
| `doe` | "Do" (body follows) |
| `gedaan` | "Done" (end of function) |

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

**Output:** `hallo wereld`

| Code | Meaning |
|------|---------|
| `maak funksie groet met wie doe` | Define function "groet" with parameter "wie" |
| `roep groet met tekst wereld amen` | Call "groet" with argument "wereld" |

### Multiple Parameters

Use `en` ("and") to separate parameters:

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

Use `geeftterug` ("give back") to return values:

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

**Output:** `8`

---

## Lesson 6: Complete Program

Let's put everything together:

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

## Common Mistakes

### 1. Forgetting `amen`

```platskript
# ❌ Wrong
klap tekst hello

# ✅ Correct
klap tekst hello amen
```

**Error message:** `'amen' vergeten!`

### 2. Forgetting `da` for Variables

```platskript
# ❌ Wrong - treats "naam" as literal text
klap naam amen

# ✅ Correct - references the variable
klap da naam amen
```

### 3. Forgetting `gedaan` to Close Blocks

```platskript
# ❌ Wrong - missing gedaan
plan doe
  klap tekst hello amen

# ✅ Correct
plan doe
  klap tekst hello amen
gedaan
```

### 4. Missing `doe` After Function Definition

```platskript
# ❌ Wrong - missing doe
maak funksie test met x
  klap da x amen
gedaan

# ✅ Correct
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

<details>
<summary>Solution</summary>

```platskript
# coding: vlaamsplats
plan doe
  zet mijnNaam op tekst Jan amen
  klap tekst Gdag plakt spatie plakt da mijnNaam plakt tekst ! amen
gedaan
```

</details>

### Exercise 2: Simple Calculator

Write a program that:
1. Stores two numbers
2. Calculates and prints their sum, difference, and product

<details>
<summary>Solution</summary>

```platskript
# coding: vlaamsplats
plan doe
  zet a op getal 15 amen
  zet b op getal 7 amen

  klap da a derbij da b amen
  klap da a deraf da b amen
  klap da a keer da b amen
gedaan
```

</details>

### Exercise 3: Greeting Function

Write a function that:
1. Takes a name and a greeting as parameters
2. Prints them together with proper spacing

<details>
<summary>Solution</summary>

```platskript
# coding: vlaamsplats
plan doe
  maak funksie begroet met groet en naam doe
    klap da groet plakt spatie plakt da naam plakt tekst ! amen
  gedaan

  roep begroet met tekst Goedendag en tekst Marie amen
  roep begroet met tekst Hallo en tekst Pieter amen
gedaan
```

</details>

---

## Language Summary

### Statements

| Statement | Syntax |
|-----------|--------|
| Print | `klap <expr> amen` |
| Assignment | `zet <var> op <expr> amen` |
| Function def | `maak funksie <name> met <params> doe ... gedaan` |
| Function call | `roep <name> met <args> amen` |
| Return | `geeftterug <expr> amen` |

### Expressions

| Expression | Syntax |
|------------|--------|
| String | `tekst hello world` |
| Number | `getal 42` |
| Variable | `da <name>` |
| Space | `spatie` |
| Concat | `<expr> plakt <expr>` |

### Operators

| Operator | Platskript |
|----------|------------|
| Add | `derbij` |
| Subtract | `deraf` |
| Multiply | `keer` |
| Divide | `gedeeld` |
| Equals | `isgelijk` |
| Not equals | `isniegelijk` |
| Greater | `isgroterdan` |
| Less | `iskleinerdan` |

---

## What's Next?

| Goal | Page |
|------|------|
| Complete syntax reference | [[Language Reference]] |
| Learn all CLI commands | [[CLI Reference]] |
| See more examples | [[Examples Gallery]] |
| Try the REPL | [[REPL Guide]] |

---

**Veel plansen!** 🧇
