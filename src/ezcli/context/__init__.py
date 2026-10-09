"""Collect basic local shell environment context."""

import os
from pathlib import Path


def get_current_directory() -> Path:
    """Return the current working directory."""
    return Path.cwd()


def get_current_shell() -> str:
    """Return the configured shell, or an empty string if unavailable."""
    return os.environ.get("SHELL", "")


def collect_context() -> dict[str, str]:
    """Collect basic environment information for command generation."""
    return {
        "current_directory": str(get_current_directory()),
        "shell": get_current_shell(),
        "operating_system": os.name,
    }
