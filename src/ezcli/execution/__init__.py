"""Controlled Bash command execution."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

from ezcli.domain.models import ExecutionStatus, SafetyResult
from ezcli.safety import check_command


@dataclass(frozen=True)
class ExecutionResult:
    """Result of a command execution attempt."""

    status: ExecutionStatus
    safety: SafetyResult
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None


def execute_command(
    command: str,
    *,
    confirmed: bool,
    cwd: Path | None = None,
    timeout: float = 30.0,
) -> ExecutionResult:
    """Execute a command only after confirmation and safety checks."""
    safety = check_command(command)

    if safety.level.value == "blocked":
        return ExecutionResult(
            status=ExecutionStatus.BLOCKED,
            safety=safety,
            stderr="Execution denied by the safety checker.",
        )

    if not confirmed:
        return ExecutionResult(
            status=ExecutionStatus.CANCELLED,
            safety=safety,
            stderr="Execution cancelled: user confirmation is required.",
        )

    try:
        completed = subprocess.run(
            ["bash", "-c", command],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""

        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")

        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            safety=safety,
            stdout=stdout,
            stderr=f"{stderr}\nCommand timed out after {timeout} seconds.".strip(),
        )
    except OSError as exc:
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            safety=safety,
            stderr=f"Could not start Bash: {exc}",
        )

    return ExecutionResult(
        status=(
            ExecutionStatus.SUCCESS
            if completed.returncode == 0
            else ExecutionStatus.FAILED
        ),
        safety=safety,
        stdout=completed.stdout,
        stderr=completed.stderr,
        exit_code=completed.returncode,
    )
