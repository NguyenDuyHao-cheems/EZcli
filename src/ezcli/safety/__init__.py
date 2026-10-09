"""Rule-based safety checks for Bash commands."""

import re

from ezcli.domain.models import SafetyLevel, SafetyResult

_BLOCKED_PATTERNS: tuple[tuple[str, str], ...] = (
    (
        r"\brm\s+[^;\n]*-[^\s;]*r[^\s;]*f|\brm\s+[^;\n]*-[^\s;]*f[^\s;]*r",
        "Recursive and forced file deletion may destroy data.",
    ),
    (
        r"\bmkfs(?:\.\w+)?\b",
        "Filesystem formatting can erase data.",
    ),
    (
        r"\bdd\s+[^;\n]*\bof=/dev/",
        "Writing directly to a device can destroy data.",
    ),
    (
        r"\bshutdown\b|\breboot\b|\bpoweroff\b",
        "This command can shut down or restart the system.",
    ),
)

_WARNING_PATTERNS: tuple[tuple[str, str], ...] = (
    (
        r"\bsudo\b",
        "This command requests elevated privileges.",
    ),
    (
        r"\bchmod\s+(-R|--recursive)\b",
        "Recursive permission changes may affect many files.",
    ),
    (
        r"\bchown\s+(-R|--recursive)\b",
        "Recursive ownership changes may affect many files.",
    ),
    (
        r">\s*/(?:etc|usr|boot|dev|proc|sys)(?:/|\s|$)",
        "This command writes to a sensitive system path.",
    ),
)


def check_command(command: str) -> SafetyResult:
    """Classify a command using basic rule-based pattern matching."""
    normalized = command.strip()

    if not normalized:
        return SafetyResult(
            level=SafetyLevel.BLOCKED,
            reasons=("Empty commands cannot be executed.",),
        )

    for pattern, reason in _BLOCKED_PATTERNS:
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            return SafetyResult(
                level=SafetyLevel.BLOCKED,
                reasons=(reason,),
            )

    warnings = tuple(
        reason
        for pattern, reason in _WARNING_PATTERNS
        if re.search(pattern, normalized, flags=re.IGNORECASE)
    )

    if warnings:
        return SafetyResult(
            level=SafetyLevel.WARNING,
            reasons=warnings,
        )

    return SafetyResult(level=SafetyLevel.SAFE)
