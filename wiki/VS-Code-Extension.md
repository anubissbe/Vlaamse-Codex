# VS Code Extension

> IDE support for Platskript development! 💻

The VlaamsCodex VS Code extension provides syntax highlighting, snippets, and integrated commands for Platskript (`.plats`) files.

---

## Installation

### From VS Code Marketplace (Recommended)

1. Open VS Code
2. Press `Ctrl+Shift+X` (Extensions panel)
3. Search for **"VlaamsCodex"** or **"Platskript"**
4. Click **Install**

### From Command Line

```bash
code --install-extension PlatsVlaamseCodex.vlaamscodex-platskript
```

### From VSIX File

1. Download the `.vsix` file from [GitHub Releases](https://github.com/brentishere41848/Vlaams-Codex/releases)
2. Open VS Code
3. Press `Ctrl+Shift+P` → "Extensions: Install from VSIX..."
4. Select the downloaded file

### Prerequisites

Make sure the VlaamsCodex CLI is installed:

```bash
pip install vlaamscodex
plats version  # Should show version
```

---

## Features

### Syntax Highlighting

The extension provides TextMate-based syntax highlighting for `.plats` files:

- **Keywords**: `plan`, `doe`, `gedaan`, `amen`, `zet`, `klap`, etc.
- **Strings**: `tekst ...` literals
- **Numbers**: `getal ...` literals
- **Comments**: `# ...` style
- **Functions**: `maak funksie`, `roep`, `geeftterug`
- **Operators**: `plakt`, `derbij`, `deraf`, `keer`, `gedeeld`

### Code Snippets

Type these prefixes and press `Tab` to expand:

| Prefix | Expands To | Description |
|--------|------------|-------------|
| `plan` | Full program skeleton | Basic program structure |
| `klap` | `klap tekst ... amen` | Print statement |
| `zet` | `zet ... op ... amen` | Variable assignment |
| `funksie` | Function definition | `maak funksie ... doe ... gedaan` |
| `roep` | `roep ... met ... amen` | Function call |
| `als` | If statement | `als ... dan doe ... gedaan` |
| `zolang` | While loop | `zolang ... doe ... gedaan` |

#### Snippet Example

Type `plan` then `Tab`:

```platskript
# coding: vlaamsplats
plan doe
  |  <-- cursor here
gedaan
```

### Integrated Commands

Access via Command Palette (`Ctrl+Shift+P`):

| Command | Description |
|---------|-------------|
| **VlaamsCodex: Run Plats File** | Execute the current file |
| **VlaamsCodex: Run Selection as Plats** | Run selected code |
| **VlaamsCodex: Show Generated Python** | Display transpiled Python |
| **VlaamsCodex: Build Plats to Python File** | Save as `.py` file |
| **VlaamsCodex: Check Plats File** | Validate syntax |
| **VlaamsCodex: Start Plats REPL** | Open interactive terminal |
| **VlaamsCodex: Show CLI Help** | Display help |
| **VlaamsCodex: Show CLI Version** | Display version |
| **VlaamsCodex: Fortune** | Random Flemish proverb |
| **VlaamsCodex: Examples (List)** | Browse examples |
| **VlaamsCodex: Init Project** | Create new project |

---

## Usage

### Running Files

1. Open a `.plats` file
2. Press `Ctrl+Shift+P`
3. Type "VlaamsCodex: Run"
4. Select **"VlaamsCodex: Run Plats File"**

Output appears in the **VlaamsCodex** output channel.

### Running Selections

1. Select some Platskript code
2. Press `Ctrl+Shift+P`
3. Select **"VlaamsCodex: Run Selection as Plats"**

### Viewing Generated Python

1. Open a `.plats` file
2. Press `Ctrl+Shift+P`
3. Select **"VlaamsCodex: Show Generated Python"**

The transpiled Python appears in the output channel.

### Checking Syntax

1. Open a `.plats` file
2. Press `Ctrl+Shift+P`
3. Select **"VlaamsCodex: Check Plats File"**

Errors and warnings appear in the output channel.

### Starting the REPL

1. Press `Ctrl+Shift+P`
2. Select **"VlaamsCodex: Start Plats REPL"**

An integrated terminal opens with the REPL running.

---

## Configuration

### Settings

Open Settings (`Ctrl+,`) and search for "vlaamscodex":

| Setting | Default | Description |
|---------|---------|-------------|
| `vlaamscodex.platsPath` | `"plats"` | Path to the `plats` CLI executable |

#### Custom CLI Path

If `plats` isn't in your PATH, set the full path:

**settings.json:**

```json
{
  "vlaamscodex.platsPath": "/usr/local/bin/plats"
}
```

Or on Windows:

```json
{
  "vlaamscodex.platsPath": "C:\\Users\\Name\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\plats.exe"
}
```

---

## Keyboard Shortcuts

The extension doesn't define default keyboard shortcuts. Add your own in `keybindings.json`:

```json
[
  {
    "key": "ctrl+shift+r",
    "command": "vlaamscodex.runPlatsFile",
    "when": "editorLangId == platskript"
  },
  {
    "key": "ctrl+shift+b",
    "command": "vlaamscodex.buildPlatsFile",
    "when": "editorLangId == platskript"
  }
]
```

---

## File Association

The extension automatically associates `.plats` files with the Platskript language.

### Manual Association

If needed, add to `settings.json`:

```json
{
  "files.associations": {
    "*.plats": "platskript"
  }
}
```

---

## Troubleshooting

### Syntax highlighting not working

1. **Check file extension:** Must be `.plats`

2. **Check language mode:** Look at status bar (bottom right), should show "Platskript"

3. **Reload extension:**
   - Press `Ctrl+Shift+P`
   - Type "Developer: Reload Window"

4. **Reinstall extension:**
   - Uninstall from Extensions panel
   - Restart VS Code
   - Install again

### Commands fail or show errors

1. **Check CLI installation:**

```bash
plats version
```

2. **Check extension setting:**
   - Open Settings
   - Search "vlaamscodex"
   - Verify `platsPath` points to valid executable

3. **Check output:**
   - View → Output
   - Select "VlaamsCodex" from dropdown
   - Look for error messages

### Snippets not appearing

1. **Trigger suggestions:** Press `Ctrl+Space` after typing prefix

2. **Check language mode:** Must be in a `.plats` file

3. **Check snippet settings:** Ensure snippets are enabled in VS Code settings

---

## Development

### Building from Source

```bash
cd vscode-extension
npm install
npm run compile
npx @vscode/vsce package
```

### Debugging

1. Open the `vscode-extension` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Open a `.plats` file in the new window
4. Test features

### Contributing

See [[Contributing]] for guidelines on contributing to the extension.

---

## Features Roadmap

Future features being considered:

- [ ] Error diagnostics (underline errors)
- [ ] Hover documentation
- [ ] Go to definition
- [ ] Code completion beyond snippets
- [ ] Debugger integration
- [ ] Format document

---

## See Also

- [[Getting Started]] - Install VlaamsCodex CLI
- [[Language Reference]] - Platskript syntax
- [[CLI Reference]] - All commands available
- [[Troubleshooting]] - More troubleshooting tips

---

**Veel plansen!** 🧇
