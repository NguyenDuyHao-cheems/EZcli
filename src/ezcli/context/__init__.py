"""Collect basic local shell environment context."""

import os
import platform
from pathlib import Path


def get_current_directory() -> Path:
    """Return the current working directory, or home directory as fallback."""
    try:
        return Path.cwd()
    except (OSError, RuntimeError):
        return Path.home()


def get_current_shell() -> str:
    """Return the configured shell, or an empty string if unavailable."""
    try:
        return os.environ.get("SHELL", "")
    except Exception:
        return ""


def get_operating_system() -> str:
    """Return the operating system name, or an empty string if unavailable."""
    try:
        return platform.system() or os.name
    except Exception:
        return "unknown"


def collect_context() -> dict[str, str]:
    """Collect basic environment information safely without crashing."""
    try:
        directory = str(get_current_directory())
    except Exception:
        directory = ""

    try:
        shell = get_current_shell()
    except Exception:
        shell = ""

    try:
        operating_system = get_operating_system()
    except Exception:
        operating_system = "unknown"

    return {
        "current_directory": directory,
        "shell": shell,
        "operating_system": operating_system,
    }
