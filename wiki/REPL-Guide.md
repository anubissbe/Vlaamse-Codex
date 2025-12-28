# REPL Guide

> Interactive Platskript exploration! 🧇

The REPL (Read-Eval-Print Loop) lets you experiment with Platskript interactively, perfect for learning and testing ideas.

---

## Starting the REPL

### Standard Command

```bash
plats repl
```

### Dialect Aliases

Use your preferred regional dialect:

| Region | Command |
|--------|---------|
| Standard | `plats repl` |
| West-Vlaams | `plats proboir` |
| Antwerps | `plats smos` |
| Limburgs | `plats efkes` |
| Brussels | `plats klansen` |
| Oost-Vlaams | `plats probeer` |
| Genks | `plats probeirme` |

**Example:**

```bash
plats smos  # Antwerp style!
```

---

## REPL Interface

When you start the REPL, you'll see:

```
🧇 Platskript REPL (type 'stop' om te stoppen)
>>>
```

The `>>>` prompt indicates the REPL is ready for your input.

### Dialect-Specific Prompts

Different dialects may show different prompts:

| Dialect | Prompt Style |
|---------|--------------|
| Standard | `>>>` |
| Antwerps | `[Sansen] >>>` |
| West-Vlaams | `[Klansen] >>>` |

---

## REPL Commands

Special commands to control the REPL:

| Command | Action |
|---------|--------|
| `stop` | Exit the REPL |
| `cls` | Clear the screen |
| `hulp` | Show help message |

**Example:**

```
>>> hulp
Platskript REPL Commands:
  stop  - Exit the REPL
  cls   - Clear screen
  hulp  - Show this help

>>> stop
👋 Tot ziens!
```

---

## Basic Session

### Variables and Expressions

```
🧇 Platskript REPL (type 'stop' om te stoppen)
>>> klap tekst hallo amen
hallo
>>> zet x op getal 5 amen
>>> klap da x amen
5
>>> zet y op getal 3 amen
>>> klap da x derbij da y amen
8
>>> stop
👋 Tot ziens!
```

### String Concatenation

```
>>> zet naam op tekst Claude amen
>>> klap tekst Hallo plakt spatie plakt da naam plakt tekst ! amen
Hallo Claude!
```

### Arithmetic

```
>>> zet a op getal 10 amen
>>> zet b op getal 4 amen
>>> klap da a derbij da b amen
14
>>> klap da a deraf da b amen
6
>>> klap da a keer da b amen
40
>>> klap da a gedeeld da b amen
2.5
```

---

## Defining Functions

You can define and call functions in the REPL:

```
>>> maak funksie dubbel met n doe
...   geeftterug da n keer getal 2 amen
... gedaan
>>> zet result op roep dubbel met getal 7 amen
>>> klap da result amen
14
```

**Note:** Multi-line input is indicated by `...` continuation prompts.

---

## Session Examples

### Calculator Session

```
>>> zet x op getal 15 amen
>>> zet y op getal 7 amen
>>> klap tekst Som: plakt spatie amen
Som:
>>> klap da x derbij da y amen
22
>>> klap tekst Verschil: plakt spatie amen
Verschil:
>>> klap da x deraf da y amen
8
```

### Greeting Function Session

```
>>> maak funksie groet met wie doe
...   klap tekst Dag plakt spatie plakt da wie plakt tekst ! amen
... gedaan
>>> roep groet met tekst wereld amen
Dag wereld!
>>> roep groet met tekst Claude amen
Dag Claude!
```

### Building Complex Expressions

```
>>> zet voornaam op tekst Jan amen
>>> zet achternaam op tekst Janssen amen
>>> zet volledig op da voornaam plakt spatie plakt da achternaam amen
>>> klap da volledig amen
Jan Janssen
```

---

## Error Handling

The REPL provides helpful error messages:

### Missing `amen`

```
>>> klap tekst hello
Error: Statement must end with 'amen'
```

### Undefined Variable

```
>>> klap da onbekend amen
Error: Variable 'onbekend' is not defined
```

### Dialect-Specific Errors

When using dialect aliases, errors come in that dialect:

```
$ plats smos
>>> klap tekst hello
Manneke, gij zijt 'amen' vergeten!
```

```
$ plats proboir
>>> klap tekst hello
Jansen, ge zijt 'amen' vergeten!
```

---

## Tips and Tricks

### 1. Use Clear Variable Names

```
>>> zet teller op getal 0 amen    # Good
>>> zet x op getal 0 amen          # Less clear
```

### 2. Build Up Gradually

Test expressions step by step:

```
>>> zet a op getal 5 amen
>>> klap da a amen
5
>>> zet b op da a keer getal 2 amen
>>> klap da b amen
10
```

### 3. Reset Variables

You can reassign variables at any time:

```
>>> zet x op getal 1 amen
>>> klap da x amen
1
>>> zet x op getal 100 amen
>>> klap da x amen
100
```

### 4. Clear Screen for Fresh Start

```
>>> cls
```

---

## Limitations

The REPL has some limitations compared to file-based programs:

| Feature | REPL | Files |
|---------|------|-------|
| Multi-line input | Supported with continuation | Full support |
| Complex programs | Better in files | Full support |
| Saving work | Manual copy | Direct save |
| Debugging | Limited | Better tools |

For complex programs, consider:
1. Prototyping in the REPL
2. Moving working code to a `.plats` file
3. Using `plats run` for the full program

---

## REPL vs File Execution

| Use REPL When | Use Files When |
|---------------|----------------|
| Learning syntax | Building complete programs |
| Testing expressions | Saving your work |
| Quick experiments | Complex logic |
| Exploring the language | Sharing code |

---

## Exiting the REPL

Type `stop` to exit:

```
>>> stop
👋 Tot ziens!
```

Or use `Ctrl+C` / `Ctrl+D` to force quit.

---

## See Also

- [[Getting Started]] - Installation and first steps
- [[Language Tutorial]] - Step-by-step learning
- [[CLI Reference]] - All command line options
- [[Examples Gallery]] - Sample programs to try

---

**Veel plansen!** 🧇
