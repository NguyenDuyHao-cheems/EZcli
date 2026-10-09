"""Tests for JSON-based command history storage."""

from datetime import datetime
from pathlib import Path

from ezcli.domain.models import ExecutionStatus, HistoryEntry, SafetyLevel
from ezcli.history import HistoryStore


def test_save_and_load_history(tmp_path: Path) -> None:
    history_file = tmp_path / "history.json"
    store = HistoryStore(history_file)
    entry = HistoryEntry(
        prompt="list files",
        command="ls -la",
        timestamp=datetime(2026, 10, 9, 12, 0, 0),
        safety=SafetyLevel.SAFE,
        status=ExecutionStatus.SUCCESS,
        exit_code=0,
    )

    store.save(entry)
    loaded_entries = store.load()

    assert loaded_entries == [entry]


def test_load_returns_empty_list_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    store = HistoryStore(tmp_path / "missing.json")

    assert store.load() == []


def test_save_appends_entries(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.json")
    first_entry = HistoryEntry(
        prompt="list files",
        command="ls",
        timestamp=datetime(2026, 10, 9, 12, 0, 0),
        safety=SafetyLevel.SAFE,
        status=ExecutionStatus.SUCCESS,
        exit_code=0,
    )
    second_entry = HistoryEntry(
        prompt="show current directory",
        command="pwd",
        timestamp=datetime(2026, 10, 9, 12, 1, 0),
        safety=SafetyLevel.SAFE,
        status=ExecutionStatus.SUCCESS,
        exit_code=0,
    )

    store.save(first_entry)
    store.save(second_entry)

    assert store.load() == [first_entry, second_entry]
