# Examples Gallery

> Learn from working Platskript programs! 📚

This gallery contains annotated examples to help you learn Platskript by reading and running real code.

---

## Running Examples

VlaamsCodex includes built-in examples you can explore directly:

```bash
# List all available examples
plats examples

# View an example's source code
plats examples --show hello

# Run an example
plats examples --run hello

# Save an example to your current directory
plats examples --save hello
```

---

## Available Examples

| Example | Description | Concepts |
|---------|-------------|----------|
| `hello` | Hello World with function | Functions, print, strings |
| `funksies` | Function definitions | Functions, parameters, calls |
| `teller` | Counter/loop | Variables, math, loops |
| `begroeting` | Greeting program | String concatenation |
| `rekenmachine` | Calculator | Arithmetic operators |

---

## Example 1: Hello World (`hello.plats`)

The classic first program, Flemish style!

```platskript
# coding: vlaamsplats
plan doe
  zet naam op tekst weeireld amen

  maak funksie groet met wie doe
    klap tekst gdag plakt spatie plakt tekst aan plakt spatie plakt da wie amen
  gedaan

  roep groet met da naam amen
gedaan
```

### Output

```
gdag aan weeireld
```

### Line-by-Line Breakdown

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `# coding: vlaamsplats` | Enable magic mode for `python file.plats` |
| 2 | `plan doe` | Start the main program block |
| 3 | `zet naam op tekst weeireld amen` | Create variable `naam` with value "weeireld" |
| 5-7 | `maak funksie groet met wie doe ... gedaan` | Define function `groet` with parameter `wie` |
| 6 | `klap tekst gdag plakt spatie plakt tekst aan plakt spatie plakt da wie amen` | Print greeting by concatenating strings |
| 9 | `roep groet met da naam amen` | Call `groet` function with `naam` variable |
| 10 | `gedaan` | End the main program block |

### Try It

```bash
plats examples --run hello
```

---

## Example 2: Functions (`funksies.plats`)

Demonstrates function definitions and calls.

```platskript
# coding: vlaamsplats
plan doe
  maak funksie zegHallo doe
    klap tekst Hallo! amen
  gedaan

  maak funksie begroet met naam doe
    klap tekst Dag plakt spatie plakt da naam plakt tekst ! amen
  gedaan

  maak funksie optellen met a en b doe
    geeftterug da a derbij da b amen
  gedaan

  roep zegHallo amen
  roep begroet met tekst Claude amen

  zet resultaat op roep optellen met getal 5 en getal 3 amen
  klap da resultaat amen
gedaan
```

### Output

```
Hallo!
Dag Claude!
8
```

### Key Concepts

1. **Function without parameters**: `maak funksie zegHallo doe`
2. **Function with one parameter**: `maak funksie begroet met naam doe`
3. **Function with multiple parameters**: `maak funksie optellen met a en b doe`
4. **Return values**: `geeftterug da a derbij da b amen`
5. **Calling functions**: `roep zegHallo amen`, `roep begroet met tekst Claude amen`

### Try It

```bash
plats examples --run funksies
```

---

## Example 3: Counter (`teller.plats`)

Demonstrates loops and counting.

```platskript
# coding: vlaamsplats
plan doe
  zet teller op getal 1 amen

  klap tekst Tellen tot 5: amen

  zolang da teller kleinerdan getal 6 doe
    klap da teller amen
    zet teller op da teller derbij getal 1 amen
  gedaan

  klap tekst Klaar! amen
gedaan
```

### Output

```
Tellen tot 5:
1
2
3
4
5
Klaar!
```

### Key Concepts

1. **Variable initialization**: `zet teller op getal 1 amen`
2. **While loop**: `zolang da teller kleinerdan getal 6 doe ... gedaan`
3. **Comparison**: `da teller kleinerdan getal 6`
4. **Increment**: `zet teller op da teller derbij getal 1 amen`

### Try It

```bash
plats examples --run teller
```

---

## Example 4: Greeting (`begroeting.plats`)

Demonstrates string concatenation.

```platskript
# coding: vlaamsplats
plan doe
  zet voornaam op tekst Jan amen
  zet achternaam op tekst Janssen amen

  klap tekst Welkom, plakt spatie plakt da voornaam plakt spatie plakt da achternaam plakt tekst ! amen

  zet volledigeNaam op da voornaam plakt spatie plakt da achternaam amen
  klap tekst Uw naam is: plakt spatie plakt da volledigeNaam amen
gedaan
```

### Output

```
Welkom, Jan Janssen!
Uw naam is: Jan Janssen
```

### Key Concepts

1. **Multiple variables**: `zet voornaam`, `zet achternaam`
2. **String concatenation**: Using `plakt` to join strings
3. **Space insertion**: Using `spatie` for readable output
4. **Building complex strings**: Storing concatenated result in variable

### Try It

```bash
plats examples --run begroeting
```

---

## Example 5: Calculator (`rekenmachine.plats`)

Demonstrates arithmetic operations.

```platskript
# coding: vlaamsplats
plan doe
  zet x op getal 10 amen
  zet y op getal 5 amen

  klap tekst Rekenmachine amen
  klap tekst =========== amen

  zet som op da x derbij da y amen
  klap tekst Som: plakt spatie plakt da som amen

  zet verschil op da x deraf da y amen
  klap tekst Verschil: plakt spatie plakt da verschil amen

  zet product op da x keer da y amen
  klap tekst Product: plakt spatie plakt da product amen

  zet quotient op da x gedeeld da y amen
  klap tekst Quotient: plakt spatie plakt da quotient amen
gedaan
```

### Output

```
Rekenmachine
===========
Som: 15
Verschil: 5
Product: 50
Quotient: 2.0
```

### Key Concepts

1. **Number literals**: `getal 10`, `getal 5`
2. **Addition**: `da x derbij da y`
3. **Subtraction**: `da x deraf da y`
4. **Multiplication**: `da x keer da y`
5. **Division**: `da x gedeeld da y`

### Try It

```bash
plats examples --run rekenmachine
```

---

## Practice: Modify These Examples

Try these modifications to deepen your understanding:

### Hello World Modifications

1. Change the greeting to your name
2. Add a second function that says goodbye
3. Call both functions in sequence

### Calculator Modifications

1. Add modulo operation (`rest`)
2. Create a function for each operation
3. Add user-friendly labels

### Counter Modifications

1. Count down instead of up
2. Count by 2s instead of 1s
3. Add a running total

---

## Write Your Own!

Ready to write your own programs? Here's a template:

```platskript
# coding: vlaamsplats
plan doe
  # Your code here!
  klap tekst Mijn eerste programma! amen
gedaan
```

Save as `mijn.plats` and run:

```bash
python mijn.plats
# or
plats run mijn.plats
```

---

## Submit Your Example

Have a cool example? Consider contributing!

1. Fork the repository
2. Add your example to `examples/`
3. Submit a pull request

See [[Contributing]] for guidelines.

---

## See Also

- [[Language Tutorial]] - Step-by-step lessons
- [[Language Reference]] - Complete syntax
- [[REPL Guide]] - Try code interactively
- [[Getting Started]] - Installation guide

---

**Veel plansen!** 🧇
