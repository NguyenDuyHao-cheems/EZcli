"""Collect and represent local shell environment context."""

from __future__ import annotations

import os
import platform
from dataclasses import asdict, dataclass
from pathlib import Path

__all__ = [
    "EnvironmentContext",
    "collect_context",
    "get_current_directory",
    "get_current_shell",
    "get_environment_context",
    "get_operating_system",
]

_FALLBACK_OS = "unknown"
_FALLBACK_SHELL = ""


@dataclass(frozen=True)
class EnvironmentContext:
    """Immutable snapshot of the local shell execution environment."""

    current_directory: str
    shell: str
    operating_system: str

    def to_dict(self) -> dict[str, str]:
        """Convert the environment snapshot into a dictionary format."""
        return asdict(self)


def get_current_directory() -> Path:
    """Return the current working directory with multi-tier fallback protection.

    Attempts to resolve Path.cwd(). If that fails due to deleted directories or
    permission constraints, falls back to the user's home directory, or root.
    """
    try:
        return Path.cwd()
    except (OSError, RuntimeError):
        try:
            return Path.home()
        except (OSError, RuntimeError):
            return Path(".")


def get_current_shell() -> str:
    """Return the active shell identifier, or an empty string if unavailable."""
    try:
        shell = os.environ.get("SHELL", _FALLBACK_SHELL)
        return shell.strip() if shell else _FALLBACK_SHELL
    except Exception:
        return _FALLBACK_SHELL


def get_operating_system() -> str:
    """Return normalized operating system name with resilient fallback.

    Uses platform.system() as the primary source, falling back to os.name,
    and finally to a safe default placeholder without raising exceptions.
    """
    try:
        system_name = platform.system()
        if system_name:
            return system_name
        return os.name or _FALLBACK_OS
    except Exception:
        return _FALLBACK_OS


def get_environment_context() -> EnvironmentContext:
    """Build an immutable, strongly-typed EnvironmentContext instance."""
    try:
        directory = str(get_current_directory())
    except Exception:
        directory = ""

    try:
        shell = get_current_shell()
    except Exception:
        shell = _FALLBACK_SHELL

    try:
        operating_system = get_operating_system()
    except Exception:
        operating_system = _FALLBACK_OS

    return EnvironmentContext(
        current_directory=directory,
        shell=shell,
        operating_system=operating_system,
    )


def collect_context() -> dict[str, str]:
    """Collect basic environment information safely as a dictionary."""
    try:
        return get_environment_context().to_dict()
    except Exception:
        return {
            "current_directory": "",
            "shell": _FALLBACK_SHELL,
            "operating_system": _FALLBACK_OS,
        }
