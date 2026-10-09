"""Tests for controlled Bash command execution."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from ezcli.domain.models import ExecutionStatus, SafetyLevel
from ezcli.execution import execute_command


def test_blocked_command_is_not_executed() -> None:
    with patch("ezcli.execution.subprocess.run") as mock_run:
        result = execute_command("rm -rf /tmp/example", confirmed=True)

    assert result.status == ExecutionStatus.BLOCKED
    mock_run.assert_not_called()


def test_unconfirmed_command_is_not_executed() -> None:
    with patch("ezcli.execution.subprocess.run") as mock_run:
        result = execute_command("ls -la", confirmed=False)

    assert result.status == ExecutionStatus.CANCELLED
    mock_run.assert_not_called()


def test_confirmed_command_executes() -> None:
    completed = subprocess.CompletedProcess(
        args=["bash", "-c", "ls -la"],
        returncode=0,
        stdout="file.txt\n",
        stderr="",
    )

    with patch(
        "ezcli.execution.subprocess.run",
        return_value=completed,
    ) as mock_run:
        result = execute_command("ls -la", confirmed=True)

    assert result.status == ExecutionStatus.SUCCESS
    assert result.safety.level == SafetyLevel.SAFE
    assert result.stdout == "file.txt\n"
    assert result.exit_code == 0
    mock_run.assert_called_once()


def test_failed_command_returns_nonzero_exit_code() -> None:
    completed = subprocess.CompletedProcess(
        args=["bash", "-c", "false"],
        returncode=1,
        stdout="",
        stderr="failed",
    )

    with patch(
        "ezcli.execution.subprocess.run",
        return_value=completed,
    ):
        result = execute_command("false", confirmed=True)

    assert result.status == ExecutionStatus.FAILED
    assert result.exit_code == 1
    assert result.stderr == "failed"


def test_execution_timeout_is_reported() -> None:
    with patch(
        "ezcli.execution.subprocess.run",
        side_effect=subprocess.TimeoutExpired(
            cmd=["bash", "-c", "sleep 60"],
            timeout=1,
        ),
    ):
        result = execute_command(
            "sleep 60",
            confirmed=True,
            timeout=1,
        )

    assert result.status == ExecutionStatus.FAILED
    assert "timed out" in result.stderr.lower()


def test_working_directory_is_passed_to_bash(tmp_path: Path) -> None:
    completed = subprocess.CompletedProcess(
        args=["bash", "-c", "pwd"],
        returncode=0,
        stdout=f"{tmp_path}\n",
        stderr="",
    )

    with patch(
        "ezcli.execution.subprocess.run",
        return_value=completed,
    ) as mock_run:
        execute_command("pwd", confirmed=True, cwd=tmp_path)

    assert mock_run.call_args.kwargs["cwd"] == tmp_path