
"""Tests for the application service."""

from pathlib import Path
from unittest.mock import patch

from ezcli.application import CommandService
from ezcli.domain.models import (
    ExecutionStatus,
    GeneratedCommand,
    SafetyLevel,
)
from ezcli.history import HistoryStore


def test_prepare_command_returns_safe_result(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.json")
    service = CommandService(history_store=store)
    generated = GeneratedCommand(
        prompt="list files",
        command="ls -la",
    )

    with patch.object(
        service._llm_client,
        "generate_command",
        return_value=generated,
    ) as mock_generate:
        prepared = service.prepare_command("list files")

    mock_generate.assert_called_once()
    assert prepared.generated == generated
    assert prepared.safety.level == SafetyLevel.SAFE


def test_prepare_command_blocks_dangerous_command(
    tmp_path: Path,
) -> None:
    service = CommandService(
        history_store=HistoryStore(tmp_path / "history.json")
    )
    generated = GeneratedCommand(
        prompt="delete files",
        command="rm -rf /tmp/example",
    )

    with patch.object(
        service._llm_client,
        "generate_command",
        return_value=generated,
    ):
        prepared = service.prepare_command("delete files")

    assert prepared.safety.level == SafetyLevel.BLOCKED


def test_record_outcome_saves_history(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.json")
    service = CommandService(history_store=store)
    generated = GeneratedCommand(
        prompt="list files",
        command="ls -la",
    )

    with patch.object(
        service._llm_client,
        "generate_command",
        return_value=generated,
    ):
        prepared = service.prepare_command("list files")

    service.record_outcome(
        prepared,
        status=ExecutionStatus.SUCCESS,
        exit_code=0,
    )

    entries = store.load()

    assert len(entries) == 1
    assert entries[0].prompt == "list files"
    assert entries[0].command == "ls -la"
    assert entries[0].safety == SafetyLevel.SAFE
    assert entries[0].status == ExecutionStatus.SUCCESS
    assert entries[0].exit_code == 0
