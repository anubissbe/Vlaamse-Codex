# AB Method Workflows

This directory contains structured workflows for common development tasks in VlaamsCodex.

## Available Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| [Update Architecture](core/update-architecture.md) | `/update-architecture` | Maintain architecture documentation |

## Usage

Workflows can be invoked via slash commands or referenced manually:

```bash
# Via Claude Code
/update-architecture

# Or reference directly
cat .ab-method/core/update-architecture.md
```

## Structure

```
.ab-method/
├── README.md           # This file
└── core/               # Core workflows
    └── update-architecture.md
```

## Adding Workflows

1. Create markdown file in appropriate subdirectory
2. Follow the workflow template structure
3. Add to this README's workflow table
4. Register slash command if applicable
