"""Tests for environment context collection."""

from pathlib import Path

import pytest

from ezcli.context import (
    collect_context,
    get_current_directory,
    get_current_shell,
    get_operating_system,
)


def test_get_current_directory() -> None:
    assert get_current_directory() == Path.cwd()


def test_get_current_directory_fallback_on_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _failing_cwd() -> Path:
        raise OSError("Permission denied")

    monkeypatch.setattr(Path, "cwd", _failing_cwd)
    assert get_current_directory() == Path.home()


def test_get_current_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHELL", "/bin/bash")

    assert get_current_shell() == "/bin/bash"


def test_get_current_shell_when_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SHELL", raising=False)

    assert get_current_shell() == ""


def test_get_operating_system() -> None:
    os_name = get_operating_system()
    assert isinstance(os_name, str)
    assert len(os_name) > 0


def test_get_operating_system_fallback_on_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _failing_system() -> str:
        raise RuntimeError("system call failed")

    monkeypatch.setattr("platform.system", _failing_system)
    monkeypatch.setattr("os.name", "")
    assert get_operating_system() == "unknown"


def test_collect_context_contains_expected_keys() -> None:
    context = collect_context()

    assert set(context) == {
        "current_directory",
        "shell",
        "operating_system",
    }
    assert context["current_directory"] == str(Path.cwd())
    assert isinstance(context["operating_system"], str)


def test_collect_context_does_not_crash_when_helpers_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _fail() -> str:
        raise RuntimeError("boom")

    monkeypatch.setattr("ezcli.context.get_current_directory", _fail)
    monkeypatch.setattr("ezcli.context.get_current_shell", _fail)
    monkeypatch.setattr("ezcli.context.get_operating_system", _fail)

    context = collect_context()
    assert isinstance(context, dict)
    assert "current_directory" in context
    assert "shell" in context
    assert "operating_system" in context
