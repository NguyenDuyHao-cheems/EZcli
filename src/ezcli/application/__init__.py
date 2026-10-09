"""Application service coordinating EZcli command generation."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ezcli.context import collect_context
from ezcli.domain.models import (
    ExecutionStatus,
    GeneratedCommand,
    HistoryEntry,
    SafetyResult,
)
from ezcli.history import HistoryStore
from ezcli.llm import OllamaClient
from ezcli.safety import check_command


@dataclass(frozen=True)
class PreparedCommand:
    """A generated command together with its safety assessment."""

    generated: GeneratedCommand
    safety: SafetyResult


class CommandService:
    """Coordinate command generation, safety checking, and history."""

    def __init__(
        self,
        llm_client: OllamaClient | None = None,
        history_store: HistoryStore | None = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._history_store = history_store or HistoryStore(
            Path.home() / ".local" / "share" / "ezcli" / "history.json"
        )

    def prepare_command(self, prompt: str) -> PreparedCommand:
        """Generate a command and assess its safety without executing it."""
        context = collect_context()
        generated = self._llm_client.generate_command(prompt, context)
        safety = check_command(generated.command)

        return PreparedCommand(
            generated=generated,
            safety=safety,
        )

    def record_outcome(
        self,
        prepared: PreparedCommand,
        status: ExecutionStatus,
        exit_code: int | None = None,
    ) -> None:
        """Persist the outcome of a command operation."""
        entry = HistoryEntry(
            prompt=prepared.generated.prompt,
            command=prepared.generated.command,
            timestamp=datetime.now().astimezone(),
            safety=prepared.safety.level,
            status=status,
            exit_code=exit_code,
        )
        self._history_store.save(entry)
