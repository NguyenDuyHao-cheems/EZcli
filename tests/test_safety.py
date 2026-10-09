"""Tests for command safety classification."""

from ezcli.domain.models import SafetyLevel
from ezcli.safety import check_command


def test_safe_command() -> None:
    result = check_command("ls -la")

    assert result.level == SafetyLevel.SAFE


def test_empty_command_is_blocked() -> None:
    result = check_command("   ")

    assert result.level == SafetyLevel.BLOCKED


def test_recursive_forced_delete_is_blocked() -> None:
    result = check_command("rm -rf /tmp/example")

    assert result.level == SafetyLevel.BLOCKED


def test_shutdown_is_blocked() -> None:
    result = check_command("shutdown now")

    assert result.level == SafetyLevel.BLOCKED


def test_sudo_command_warns() -> None:
    result = check_command("sudo apt update")

    assert result.level == SafetyLevel.WARNING
