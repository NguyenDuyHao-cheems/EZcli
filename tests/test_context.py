"""Tests for environment context collection."""

from pathlib import Path

import pytest

from ezcli.context import (
    collect_context,
    get_current_directory,
    get_current_shell,
)


def test_get_current_directory() -> None:
    assert get_current_directory() == Path.cwd()


def test_get_current_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHELL", "/bin/bash")

    assert get_current_shell() == "/bin/bash"


def test_get_current_shell_when_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SHELL", raising=False)

    assert get_current_shell() == ""


def test_collect_context_contains_expected_keys() -> None:
    context = collect_context()

    assert set(context) == {
        "current_directory",
        "shell",
        "operating_system",
    }
    assert context["current_directory"] == str(Path.cwd())
