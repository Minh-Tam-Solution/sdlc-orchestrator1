# sdlcctl - SDLC 5.0.0 Structure Validator CLI

A command-line tool to validate, fix, and generate SDLC 5.0.0 compliant project structures.

## Installation

### From PyPI (Recommended)

```bash
pip install sdlcctl
```

### From Source

```bash
git clone https://github.com/Minh-Tam-Solution/SDLC-Orchestrator.git
cd SDLC-Orchestrator/backend
pip install -e .
```

### Using pipx (Isolated Environment)

```bash
pipx install sdlcctl
```

## Quick Start

```bash
# Show help
sdlcctl --help

# Show version
sdlcctl --version

# Validate a project
sdlcctl validate --path /path/to/project --tier lite

# Initialize new project structure
sdlcctl init --path /path/to/new-project --tier standard

# Auto-fix structure issues
sdlcctl fix --path /path/to/project

# Generate compliance report
sdlcctl report --path /path/to/project --format markdown

# Show SDLC stages
sdlcctl stages

# Show tier requirements
sdlcctl tiers

# Generate code from natural language (Vietnamese/English)
sdlcctl magic "Tạo ứng dụng quản lý nhà hàng"
```

## Commands

| Command | Description |
|---------|-------------|
| `validate` | Validate SDLC 5.0.0 folder structure |
| `fix` | Automatically fix structure issues |
| `init` | Initialize new project structure |
| `report` | Generate compliance report |
| `migrate` | Migrate from SDLC 4.9.x to 5.0.0 |
| `generate` | Generate code from AppBlueprint |
| `magic` | Generate app from natural language |
| `stages` | Show SDLC 5.0.0 stage definitions |
| `tiers` | Show tier classification |
| `p0` | Show P0 artifact requirements |

## Tier Classification

| Tier | Team Size | Required Stages | P0 Artifacts |
|------|-----------|-----------------|--------------|
| LITE | 1-2 | 4 | No |
| STANDARD | 3-10 | 6 | No |
| PROFESSIONAL | 10-50 | 10 | Yes |
| ENTERPRISE | 50+ | 11 | Yes |

## Requirements

- Python 3.10+
- typer
- rich
- pyyaml

## License

Apache-2.0

## Links

- [Documentation](https://github.com/Minh-Tam-Solution/SDLC-Orchestrator/blob/main/docs)
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=sdlc-orchestrator)
- [GitHub](https://github.com/Minh-Tam-Solution/SDLC-Orchestrator)
