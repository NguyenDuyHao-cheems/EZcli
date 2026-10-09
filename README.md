# EZcli

EZcli is a user-friendly terminal interface for working with the command line, powered by a locally hosted AI model through Ollama.

## Overview

EZcli aims to help users generate and understand Bash commands from natural-language requests. It provides a terminal-based interface, checks generated commands for potential risks, and asks for confirmation before execution.

## Planned Features

- Generate Bash commands from natural-language input using a local AI model.
- Collect relevant environment context.
- Check commands for potential safety risks.
- Display commands and explanations before execution.
- Require user confirmation before executing commands.
- Store command history locally.

## Technology Stack

- **Language:** Python 3.12+
- **Package and environment management:** uv
- **Terminal UI:** Textual
- **CLI framework:** Typer
- **Local AI runtime:** Ollama
- **Testing:** pytest
- **Code quality:** Ruff, mypy, pre-commit

## Requirements

- Python 3.12 or later
- uv
- Ollama
- A compatible local model, planned to be `qwen2.5-coder:3b`

## Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/NguyenDuyHao-cheems/EZcli.git
cd EZcli
```

Install the project and development dependencies:

```bash
uv sync --group dev
```

Ensure Ollama is installed and the required model is available before using AI-powered features.

## Usage

Launch EZcli with:

```bash
uv run ezcli
```

The interactive interface and AI-powered workflow are under development. Usage instructions will be updated as features become available.

## Project Documentation

See the [`docs/`](docs/) directory for the project plan and software requirements.

## Development

Run code-quality checks with:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pre-commit run --all-files
```

## Safety

EZcli is designed to check generated commands and require confirmation before execution. Safety checks cannot guarantee that every dangerous command will be detected. Review commands carefully before approving their execution.

## License

See [LICENSE](LICENSE) for license information.
